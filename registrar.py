#!/usr/bin/env python

from cfg.read import read_cfg
import json
import socket
import threading

# TODO: Move handle_session to a specialized module.
# TODO: Document handle_session.
def handle_session(conn):
	msg = recv_msg(conn)
	# TODO: Redesign logic flow. Excessive if/elif statements should not be
	# used. Maybe develop a function for each message type's response?
	try:
		if msg['type'] == 'IDENT':
			if msg['content'][0] == 'registrant':
				# TODO: React and respond appropriately. This is only a
				# placeholder message.
				send_msg(conn, message('STATUS', '10001'))
			elif msg['content'][0] == 'resolver':
				# TODO: React and respond appropriately. This is only a
				# placeholder message.
				send_msg(conn, message('STATUS', '20001'))
			else:
				# Client type not recognized.
				send_msg(conn, message('STATUS', '50001'))
		else:
			raise ValueError('Message type not recognized.')
	except:
		send_msg(conn, message('STATUS', '50000'))
	finally:
		conn.close()

# TODO: Move message to a specialized module.
# TODO: Document message.
def message(msg_type, *msg_content):
	return {
		'type': msg_type,
		'content': msg_content
	}

# TODO: Move recv_msg to a specialized module.
# TODO: Document recv_msg.
def recv_msg(conn):
	# Retrieve JSON content length.
	json_len_buf = ''
	char_buf = conn.recv(1)
	while char_buf != '{':
		json_len_buf += char_buf
		char_buf = conn.recv(1)
	json_len = int(json_len_buf)
	
	# Retrieve raw JSON string.
	raw_msg = '{' + conn.recv(json_len)
	
	# Return decoded JSON object as dict.
	return json.loads(raw_msg)

# TODO: Move send_msg to a specialized module.
# TODO: Document send_msg.
def send_msg(conn, msg_dict):
	json_content = json.dumps(msg_dict)
	json_len = len(json_content)
	conn.sendall(str(json_len) + json_content)

if __name__ == '__main__':
	cfg = read_cfg('res/json/cfg.json')
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# TODO: Change `''` to `cfg['host']['hostname']`.
	sock.bind(('', cfg['host']['port']))
	sock.listen(1)
	
	while True:
		conn, addr = sock.accept()
		
		t = threading.Thread(target=handle_session, args=(conn,))
		t.daemon=True
		t.start()
