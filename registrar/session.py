import conn

# TODO: Document handle_session.
def handle_session(sock, cfg):
	msg = conn.recv_msg(sock)
	# TODO: Redesign logic flow. Excessive if/elif statements should not be
	# used. Maybe develop a function for each message type's response?
	try:
		if msg['type'] == 'IDENT':
			if msg['content'][0] == 'registrant':
				# TODO: React and respond appropriately. This is only a
				# placeholder message.
				conn.send_msg(sock, conn.message('STATUS', '10001'))
			elif msg['content'][0] == 'resolver':
				# TODO: React and respond appropriately. This is only a
				# placeholder message.
				conn.send_msg(sock, conn.message('STATUS', '20001'))
			else:
				# Client type not recognized.
				conn.send_msg(sock, conn.message('STATUS', '50001'))
		else:
			raise ValueError('Message type not recognized.')
	except:
		conn.send_msg(sock, conn.message('STATUS', '50000'))
	finally:
		sock.close()
