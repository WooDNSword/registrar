import json
import session
import socket
import threading

# TODO: Document initiate.
def initiate(cfg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# TODO: Change `''` to `cfg['host']['hostname']`.
	sock.bind(('', cfg['host']['port']))
	sock.listen(1)
	
	while True:
		conn, addr = sock.accept()
		
		t = threading.Thread(
			target=session.handle_session, args=(conn, cfg)
		)
		t.daemon=True
		t.start()

# TODO: Document message.
def message(msg_type, *msg_content):
	return {
		'type': msg_type,
		'content': msg_content
	}

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

# TODO: Document send_msg.
def send_msg(conn, msg_dict):
	json_content = json.dumps(msg_dict)
	json_len = len(json_content)
	conn.sendall(str(json_len) + json_content)
