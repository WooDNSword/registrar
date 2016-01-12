#!/usr/bin/env python

from cfg import read_cfg
from session import handle_session
import os
import socket
import threading

if __name__ == '__main__':
	# os.path module shit deals with Python's idiotic file path mechanisms.
	cfg = read_cfg(
		os.path.dirname(
			os.path.realpath(__file__)
		) + '/res/json/cfg.json'
	)
	
	# TODO: Move connection stuff into connection module (duh).
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# TODO: Change `''` to `cfg['host']['hostname']`.
	sock.bind(('', cfg['host']['port']))
	sock.listen(1)
	
	while True:
		conn, addr = sock.accept()
		
		t = threading.Thread(target=handle_session, args=(conn, cfg))
		t.daemon=True
		t.start()
