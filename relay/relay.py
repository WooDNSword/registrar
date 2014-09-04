#!/usr/bin/env python3
#
# LeanDNS Relay
# relay.py

import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ("localhost", 55555)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(host)
sock.listen(1)

domains = {}
servers = {}
threads = {}

def handleConnection(conn, addr):
	try:
		print("Connection from ", addr)
		while (True):
			data = conn.recv(1024)
			print(data)
			if (data.endswith(b"\n")):
				break
	finally:
		conn.close()

print("Listening for connections...")
try:
	while (True):
		(conn, client_addr) = sock.accept()
		servers[conn] = []
		threads[conn] = threading.Thread(target=handleConnection, args=(conn, client_addr))
		threads[conn].start()
finally:
	for conn, thread in threads.items():
		thread.join()

