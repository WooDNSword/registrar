#!/usr/bin/env python3
#
# LeanDNS Relay
# relay.py

import json
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ("localhost", 55555)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(host)
sock.listen(1)

domains = {}
servers = {}
clients = {}
threads = {}

def handleConnection(conn, addr):
	try:
		print("Connection from ", addr)
		client_type = ""
		while (True):
			data = ""
			while (True):
				data += conn.recv(512).decode("utf-8")
				if (data.endswith("\n")):
					break
			for line in [line for line in data.split("\n") if line != ""]:
				print(line)
				msg = json.loads(line)
				if (msg["type"] == "client info"):
					client_type = msg["client type"]
					if (client_type == "server"):
						servers[conn] = set()
					if (client_type == "client"):
						clients[conn] = []
				elif (msg["type"] == "quit"):
					break
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

