import conn

registrant_name = 'registrant'
resolver_name = 'resolver'

# TODO: Document cmd_ident.
def cmd_ident(globs, locs):
	client_type = locs['msg']['content'][0]
	try:
		{
			registrant_name: register_registrant,
			resolver_name: register_resolver
		}[client_type](globs, locs)
	except KeyError:
		# Client type not recognized.
		conn.send_msg(locs['sock'], conn.msg('STATUS', '50001'))

# TODO: Document deregister_client.
def deregister_client(globs, port):
	try:
		del globs['clients'][port]
	except:
		pass

# TODO: Document handle_session.
def handle_session(globs, locs):
	try:
		while True:
			locs['msg'] = conn.recv_msg(locs['sock'])
			try:
				{
					'IDENT': cmd_ident
				}[locs['msg']['type']](globs, locs)
				if locs['msg']['type'] == 'IDENT':
					cmd_ident(globs, locs)
				else:
					raise ValueError('Message type not recognized.')
			except KeyError:
				# TODO: Specify actual status code for this error.
				conn.send_msg(locs['sock'], conn.msg(
					'STATUS',
					'Unspecified error: Message type not recognized.'
				))
			except:
				# Undefined error.
				conn.send_msg(locs['sock'], conn.msg('STATUS', '50000'))
	except:
		if globs['cfg']['debug']:
			print('An error occurred. Perhaps the connection closed?')
	finally:
		deregister_client(globs, locs['addr']['port'])
		locs['sock'].close()

# TODO: Document register_client.
def register_client(globs, port, client_type):
	globs['clients'][port] = client_type

# TODO: Document register_registrant.
def register_registrant(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		register_client(globs, locs['addr']['port'], registrant_name)
		# Success!
		conn.send_msg(locs['sock'], conn.msg('STATUS', '1000'))
	except:
		# Undefined error.
		conn.send_msg(locs['sock'], conn.msg('STATUS', '10000'))

# TODO: Document register_resolver.
def register_resolver(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		register_client(globs, locs['addr']['port'], resolver_name)
		# Success!
		conn.send_msg(locs['sock'], conn.msg('STATUS', '2000'))
	except:
		# Undefined error.
		conn.send_msg(locs['sock'], conn.msg('STATUS', '20000'))
