# TODO: Document the module!
# TODO: Clean this shit the hell up. More modules, yo.
# TODO: Write tests.
# TODO: Add debug printing.
# TODO: Move status codes into their own module. We shouldn't be hard-coding
# them throughout the whole program. They need semantic identifiers.

import conn
import network

# TODO: Document cmd_ident.
def cmd_ident(globs, locs):
	client_type = locs['msg']['content'][0]
	try:
		{
			network.registrant_name: register_registrant,
			network.resolver_name: register_resolver
		}[client_type](globs, locs)
	except KeyError:
		# Client type not recognized.
		conn.send_msg(get_client_sock(locs), conn.msg('STATUS', '50001'))

# TODO: Document deregister_client.
def deregister_client(globs, locs):
	try:
		del globs['clients'][get_client_port(locs)]
		del locs['client_type']
	except:
		pass

# TODO: Document get_client_ip.
def get_client_ip(locs):
	return locs['addr']['ip']

# TODO: Document get_client_port.
def get_client_port(locs):
	return locs['addr']['port']

# TODO: Document get_client_sock.
def get_client_sock(locs):
	return locs['sock']

# TODO: Document get_client_type.
def get_client_type(locs):
	try:
		return locs['client_type']
	except:
		return network.unidentified_client_name

# TODO: Document handle_session.
def handle_session(globs, locs):
	try:
		while True:
			# TODO: Make this shit timeout for fucks' sakes. This is messing up
			# deregistration because it's not throwing an error when the remote
			# endpoint closes.
			locs['msg'] = conn.recv_msg(get_client_sock(locs))
			try:
				{
					'IDENT': cmd_ident
				}[locs['msg']['type']](globs, locs)
			except KeyError:
				# Message type not recognized.
				conn.send_msg(
					get_client_sock(locs),
					conn.msg(
						'STATUS',
						status_code_class(locs) + 'F001'
					)
				)
			except:
				# Undefined error.
				conn.send_msg(
					get_client_sock(locs),
					conn.msg('STATUS', '50000')
				)
	except:
		if globs['cfg']['debug']:
			print('An error occurred. Perhaps the connection closed?')
	finally:
		deregister_client(globs, locs)
		get_client_sock(locs).close()

# TODO: Document register_client.
def register_client(globs, locs, client_type):
	globs['clients'][get_client_port(locs)] = client_type
	locs['client_type'] = client_type

# TODO: Document register_registrant.
def register_registrant(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		register_client(globs, locs, network.registrant_name)
		# Success!
		conn.send_msg(get_client_sock(locs), conn.msg('STATUS', '1000'))
	except:
		# Undefined error.
		conn.send_msg(get_client_sock(locs), conn.msg('STATUS', '10000'))

# TODO: Document register_resolver.
def register_resolver(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		register_client(globs, locs, network.resolver_name)
		# Success!
		conn.send_msg(get_client_sock(locs), conn.msg('STATUS', '2000'))
	except:
		# Undefined error.
		conn.send_msg(get_client_sock(locs), conn.msg('STATUS', '20000'))

# TODO: Document status_code_class.
# TODO: Get rid of this shit and use the status module.
def status_code_class(locs):
	return {
		network.registrant_name: '1',
		network.resolver_name: '2',
		network.unidentified_client_name: '5'
	}[get_client_type(locs)]
