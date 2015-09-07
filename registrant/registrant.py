#!/usr/bin/env python3
#
# WooDNSword Registrant
# registrant.py

import json
import socket

f_cfg = open("registrant.cfg")
cfg = eval(f_cfg.read())
f_cfg.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(cfg["registrar"])

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
	sent_client_info = False
	while (True):
		for line in [line for line in recv().split("\n") if line != ""]:
			if (cfg["debug"]):
				print(line)
			msg = json.loads(line)
			if (msg["type"] == "ping"):
				pong(msg["id"])
				if (not sent_client_info):
					send({
						"type": "client info",
						"client type": "registrant"})
					print("Requesting domains: %s" % ', '.join([("'%s'" % domain[0]) for domain in cfg["domains"]]))
					send({
						"type": "domain request",
						"domains": cfg["domains"]})
					sent_client_info = True
			elif (msg["type"] == "status"):
				print_status(msg["code"], msg["description"])
finally:
	send({"type": "quit"})
	sock.close()

