# TODO: Document the module!
# TODO: Write tests.
# TODO: Add debug printing.

import conn
import network
import status

# TODO: Document cmdIdent.
def cmdIdent(globs, locs):
	client_type = locs['msg']['content'][0]
	try:
		{
			network.registrant_name: registerRegistrant,
			network.resolver_name: registerResolver
		}[client_type](globs, locs)
	except KeyError:
		# Client type not recognized.
		conn.sendMsg(getClientSock(locs), conn.msg(
			'STATUS',
			status.error(
				source=network.registrar_name,
				destination=getClientType(locs),
				code_class='ident',
				code_name='client identification type invalid'
			)
		))

# TODO: Document deregisterClient.
def deregisterClient(globs, locs):
	try:
		del globs['clients'][getClientPort(locs)]
		del locs['client_type']
	except:
		pass

# TODO: Document getClientIp.
def getClientIp(locs):
	return locs['addr']['ip']

# TODO: Document getClientPort.
def getClientPort(locs):
	return locs['addr']['port']

# TODO: Document getClientSock.
def getClientSock(locs):
	return locs['sock']

# TODO: Document getClientType.
def getClientType(locs):
	try:
		return locs['client_type']
	except:
		return network.unidentified_client_name

# TODO: Document handleSession.
def handleSession(globs, locs):
	try:
		while True:
			# TODO: Make this shit timeout for fucks' sakes. This is messing up
			# deregistration because it's not throwing an error when the remote
			# endpoint closes.
			locs['msg'] = conn.recvMsg(getClientSock(locs))
			try:
				{
					'IDENT': cmdIdent
				}[locs['msg']['type']](globs, locs)
			except KeyError:
				# Message type not recognized.
				conn.sendMsg(getClientSock(locs), conn.msg(
					'STATUS',
					status.error(
						source=network.registrar_name,
						destination=getClientType(locs),
						code_class='misc',
						code_name='message type invalid'
					)
				))
			except:
				# Undefined error.
				conn.sendMsg(getClientSock(locs), conn.msg(
					'STATUS',
					status.error(
						source=network.registrar_name,
						destination=getClientType(locs),
						code_class='misc',
						code_name='undefined'
					)
				))
	except:
		if globs['cfg']['debug']:
			print('An error occurred. Perhaps the connection closed?')
	finally:
		deregisterClient(globs, locs)
		getClientSock(locs).close()

# TODO: Document registerClient.
def registerClient(globs, locs, client_type):
	try:
		globs['clients'][getClientPort(locs)] = client_type
		locs['client_type'] = client_type
		# Success!
		# TODO: Change this from 'undefined' to something more semantic.
		status_message = conn.msg(
			'STATUS',
			status.success(
				source=network.registrar_name,
				destination=getClientType(locs),
				code_class='misc',
				code_name='undefined'
			)
		)
	except:
		# Undefined error.
		status_message = conn.msg(
			'STATUS',
			status.error(
				source=network.registrar_name,
				destination=getClientType(locs),
				code_class='ident',
				code_name='undefined'
			)
		)
	finally:
		conn.sendMsg(getClientSock(locs), status_message)

# TODO: Document registerRegistrant.
def registerRegistrant(globs, locs):
	# TODO: Add 'if' clause for when not accepting new registrants.
	registerClient(globs, locs, network.registrant_name)

# TODO: Document registerResolver.
def registerResolver(globs, locs):
	# TODO: Add 'if' clause for when not accepting new resolvers.
	registerClient(globs, locs, network.resolver_name)
