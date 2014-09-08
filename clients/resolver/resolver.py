#!/usr/bin/env python3
#
# LeanDNS Command-line Resolver
# resolver.py

import json
import socket
import sys

domain_to_lookup = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 55555))

def print_status(code, message):
	print("STATUS %d: %s" % (code, message))

def send(data):
	sock.send((json.dumps(data) + "\n").encode("utf-8"))

def recv():
	data = ""
	while (True):
		data += sock.recv(512).decode("utf-8")
		if (data.endswith("\n")):
			return data

def pong(identifier):
	send({"type": "pong", "id": identifier})

try:
	running = True
	sent_client_info = False
	while (running):
		for line in [line for line in recv().split("\n") if line != ""]:
			msg = json.loads(line)
			if (msg["type"] == "ping"):
				pong(msg["id"])
				if (not sent_client_info):
					send({"type": "client info", "client type": "client"})
					send({"type": "domain lookup", "domain": domain_to_lookup})
			elif (msg["type"] == "host response"):
				print(msg["address"])
				running = False
			elif (msg["type"] == "status"):
				print_status(msg["code"], msg["description"])
				running = False
finally:
	send({"type": "quit"})
	sock.close()
