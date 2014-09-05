#!/usr/bin/env python3
#
# LeanDNS Server
# server.py

import json
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ("localhost", 55555)

sock.connect(host)

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
	sent_client_info = False
	while (True):
		for line in [line for line in recv().split("\n") if line != ""]:
			print(line)
			msg = json.loads(line)
			if (msg["type"] == "ping"):
				pong(msg["id"])
				if (not sent_client_info):
					send({
						"type": "client info",
						"client type": "server"})
					send({
						"type": "domain request",
						"domains": [
							["google.com", "64.233.185.139"],
							["youtube.com", "64.233.185.93"]]})
					sent_client_info = True
finally:
	sock.close()

