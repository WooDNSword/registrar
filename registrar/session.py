# TODO: Document the module!
# TODO: Clean this shit the hell up. More modules, yo.
# TODO: Write tests.
# TODO: Add debug printing.
# TODO: Move status codes into their own module. We shouldn't be hard-coding
# them throughout the whole program. They need semantic identifiers.

import conn
import network

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
		conn.sendMsg(getClientSock(locs), conn.msg('STATUS', '50001'))

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
				conn.sendMsg(
					getClientSock(locs),
					conn.msg(
						'STATUS',
						statusCodeClass(locs) + 'F001'
					)
				)
			except:
				# Undefined error.
				conn.sendMsg(
					getClientSock(locs),
					conn.msg('STATUS', '50000')
				)
	except:
		if globs['cfg']['debug']:
			print('An error occurred. Perhaps the connection closed?')
	finally:
		deregisterClient(globs, locs)
		getClientSock(locs).close()

# TODO: Document registerClient.
def registerClient(globs, locs, client_type):
	globs['clients'][getClientPort(locs)] = client_type
	locs['client_type'] = client_type

# TODO: Document registerRegistrant.
def registerRegistrant(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		registerClient(globs, locs, network.registrant_name)
		# Success!
		conn.sendMsg(getClientSock(locs), conn.msg('STATUS', '1000'))
	except:
		# Undefined error.
		conn.sendMsg(getClientSock(locs), conn.msg('STATUS', '10000'))

# TODO: Document registerResolver.
def registerResolver(globs, locs):
	# TODO: Add except clause for when not accepting new registrants.
	try:
		registerClient(globs, locs, network.resolver_name)
		# Success!
		conn.sendMsg(getClientSock(locs), conn.msg('STATUS', '2000'))
	except:
		# Undefined error.
		conn.sendMsg(getClientSock(locs), conn.msg('STATUS', '20000'))

# TODO: Document statusCodeClass.
# TODO: Get rid of this shit and use the status module.
def statusCodeClass(locs):
	return {
		network.registrant_name: '1',
		network.resolver_name: '2',
		network.unidentified_client_name: '5'
	}[getClientType(locs)]
