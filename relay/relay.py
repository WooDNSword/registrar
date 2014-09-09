#!/usr/bin/env python3
#
# LeanDNS Relay
# relay.py

import json
import random
import socket
import threading
import time

f_cfg = open("relay.cfg")
cfg = eval(f_cfg.read())
f_cfg.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(cfg["host"])
sock.listen(1)

domains = {}
servers = {"localhost": set()}
clients = {}
threads = {}

def print_status(code, message):
	print("STATUS %d: %s" % (code, message))

def send(conn, data):
	msg = json.dumps(data) + "\n"
	conn.send(msg.encode("utf-8"))
	if (cfg["debug"]):
		print("Sending %s to" % msg, conn)

def recv(conn):
	data = ""
	while (True):
		data += conn.recv(512).decode("utf-8")
		if (data.endswith("\n")):
			return data

def add_domains(conn, owner, domain_list, overwrite):
	if (owner in cfg["blacklist"]["owners"]):
		if (conn == "localhost"):
			print_status(201, "Owner '%s' is blacklisted." % owner)
		else:
			send(conn, {"type": "status", "code": 201, "description": "Owner '%s' is blacklisted." % owner})
	else:
		for domain in domain_list:
			result_code = 0
			result_text = ""
			(domain_name, domain_addr) = domain
			if (domain_addr == "localhost"):
				domain_addr = owner
			if (domain_name in cfg["blacklist"]["domains"]):
				result_code = 202
				result_text = "Domain name '%s' is blacklisted." % domain_name
			elif (domain_addr in cfg["blacklist"]["addresses"]):
				result_code = 203
				result_text = "Address '%s' is blacklisted." % domain_addr
			elif (domain_name not in domains or overwrite):
				servers[conn].update({domain_name})
				domains[domain_name] = {"addr": domain_addr, "owner": owner}
				result_code = 100
				result_text = "Domain name '%s' -> '%s' successfully claimed." % (domain_name, domain_addr)
			else:
				result_code = 301
				result_text = "Domain name '%s' is already taken." % domain_name
			if (conn == "localhost"):
				print_status(result_code, result_text)
			else:
				send(conn, {"type": "status", "code": result_code, "description": result_text})
		if (cfg["debug"]):
			print("Domains: %s" % repr(domains))
			print("Servers: %s" % repr(servers))

def handleConnection(conn, addr):
	running = [True]
	def ping(ping_pending):
		if (ping_pending[0]):
			raise IOError("ping timeout")
		print("pinging...")
		identifier = random.randint(10000, 99999)
		send(conn, {"type": "ping", "id": identifier})
		ping_pending[0] = identifier
	def pingLoop(running, ping_pending):
		while (running[0]):
			try:
				ping(ping_pending)
			except IOError as e:
				print("IOError:", e)
				running[0] = False
				break
			time.sleep(cfg["ping interval"])
	try:
		print("Connection from ", addr)
		ping_pending = [False] # Must be mutable
		ping_thread = threading.Thread(target=pingLoop, args=(running, ping_pending))
		ping_thread.start()
		client_type = ""
		while (running[0]):
			for line in [line for line in recv(conn).split("\n") if line != ""]:
				if (cfg["debug"]):
					print(line)
				msg = json.loads(line)
				if (msg["type"] == "client info"):
					client_type = msg["client type"]
					if (client_type == "server"):
						servers[conn] = set()
					if (client_type == "client"):
						clients[conn] = []
				elif (msg["type"] == "pong"):
					if (ping_pending[0] and ping_pending[0] == msg["id"]):
						ping_pending[0] = False
				elif (msg["type"] == "status"):
					print_status(msg["code"], msg["description"])
				elif (msg["type"] == "quit"):
					running[0] = False
				elif (client_type == "server"):
					if (msg["type"] == "domain request"):
						add_domains(conn, addr[0], msg["domains"], False)
				elif (client_type == "client"):
					if (msg["type"] == "domain lookup"):
						if (msg["domain"] in domains):
							send(conn, {"type": "host response", "address": domains[msg["domain"]]["addr"]})
						else:
							send(conn, {"type": "status", "code": 401, "description": "Domain '%s' lookup failed." % msg["domain"]})
	finally:
		if conn in servers.keys():
			for domain in servers[conn]:
				if domain in domains.keys():
					del domains[domain]
			del servers[conn]
		if conn in clients:
			del clients[conn]
		ping_thread.join()
		conn.close()

add_domains("localhost", "localhost", cfg["registered domains"], True)

print("Listening for connections...")
try:
	while (True):
		(conn, client_addr) = sock.accept()
		threads[conn] = threading.Thread(target=handleConnection, args=(conn, client_addr))
		threads[conn].start()
finally:
	for conn, thread in threads.items():
		thread.join()

