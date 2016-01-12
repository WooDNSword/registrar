from connection import message, recv_msg, send_msg

# TODO: Document handle_session.
def handle_session(conn, cfg):
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
