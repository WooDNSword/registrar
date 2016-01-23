# TODO: Document the module!
# TODO: Move this module into an independent repository (DRY principle: more
# than one repository uses equivalent code.

import network

# All but first character of a STATUS code.
code_tails = {
	'error': {
		'ident': (
			'0',
			{
				'undefined': '000',
				'client type access prohibited': '001',
				'client identification type prohibited': '002',
				'client identification type invalid': '003'
			}
		),
		'misc': (
			'F',
			{
				'undefined': '000',
				'message type invalid': '001'
			}
		)
	},
	'success': {
		'misc': (
			'0',
			{
				'undefined': '00'
			}
		)
	}
}

# First character of a STATUS code.
direction_char = {
	(network.registrar_name, network.registrant_name): '1',
	(network.registrar_name, network.resolver_name): '2',
	(network.registrant_name, network.registrar_name): '3',
	(network.resolver_name, network.registrar_name): '4',
	(network.registrar_name, network.unidentified_client_name): '5',
	(network.unidentified_client_name, network.registrar_name): '6'
}

# TODO: Document Error.
def Error(
	source=None,
	destination=None,
	code_class=None,
	code_name=None
	):
	return ConstructStatus(
		source=source,
		destination=destination,
		code_type='error',
		code_class=code_class,
		code_name=code_name
	)

# TODO: Document ConstructStatus.
# Don't call this externally.
def ConstructStatus(
	source=None,
	destination=None,
	code_type=None,
	code_class=None,
	code_name=None
	):
	# Generate first digit of STATUS code (direction).
	status_code = direction_char[(source, destination)]
	
	# Generate them other digits, yo.
	status_code_class = code_tails[code_type][code_class]
	status_code += status_code_class[0] + status_code_class[1][code_name]
	
	return status_code

# TODO: Document Success.
def Success(
	source=None,
	destination=None,
	code_class=None,
	code_name=None
	):
	return ConstructStatus(
		source=source,
		destination=destination,
		code_type='success',
		code_class=code_class,
		code_name=code_name
	)
