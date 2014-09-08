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
servers = {}
clients = {}
threads = {}

def send(conn, data):
	conn.send((json.dumps(data) + "\n").encode("utf-8"))

def recv(conn):
	data = ""
	while (True):
		data += conn.recv(512).decode("utf-8")
		if (data.endswith("\n")):
			return data

def handleConnection(conn, addr):
	running = True
	def ping(ping_pending):
		if (ping_pending[0]):
			raise IOError("ping timeout")
		print("pinging...")
		identifier = random.randint(10000, 99999)
		send(conn, {"type": "ping", "id": identifier})
		ping_pending[0] = identifier
	def pingLoop(ping_pending):
		while (running):
			ping(ping_pending)
			time.sleep(180)
	try:
		print("Connection from ", addr)
		ping_pending = [False] # Must be mutable
		print(ping_pending)
		ping_thread = threading.Thread(target=pingLoop, args=[ping_pending])
		ping_thread.start()
		client_type = ""
		while (running):
			for line in [line for line in recv(conn).split("\n") if line != ""]:
				print(line)
				msg = json.loads(line)
				if (msg["type"] == "client info"):
					client_type = msg["client type"]
					if (client_type == "server"):
						servers[conn] = set()
					if (client_type == "client"):
						clients[conn] = []
				elif (msg["type"] == "pong"):
					pass
					if (ping_pending[0] and ping_pending[0] == msg["id"]):
						ping_pending[0] = False
				elif (msg["type"] == "quit"):
					running = False
				elif (client_type == "server"):
					if (msg["type"] == "domain request"):
						for domain in msg["domains"]:
							(domain_name, domain_addr) = domain
							servers[conn].update({domain_name})
							domains[domain_name] = {"addr": domain_addr, "owner": addr}
						print("Domains: %s" % repr(domains))
						print("Servers: %s" % repr(servers))
				elif (client_type == "client"):
					pass
	finally:
		ping_thread.join()
		if conn in domains:
			del domains[conn]
		if conn in servers:
			del servers[conn]
		if conn in clients:
			del clients[conn]
		conn.close()

print("Listening for connections...")
try:
	while (True):
		(conn, client_addr) = sock.accept()
		threads[conn] = threading.Thread(target=handleConnection, args=(conn, client_addr))
		threads[conn].start()
finally:
	for conn, thread in threads.items():
		thread.join()

