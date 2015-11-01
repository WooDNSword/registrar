/**
 * Accept a hostname and a port, then concatenate them together in that order,
 * conjoined by a colon (':'), and return the result.
 * 
 * For example, `endpointToString('127.0.0.1', 8080)` will return the string
 * '127.0.0.1:8080'.
 */
exports.endpointToString = function (endpoint) {
	return endpoint.host + ':' + endpoint.port;
}

/**
 * Accept a string of the format '<host>:<port>', such as '127.0.0.1:8080', and
 * return an endpoint object.
 */
exports.stringToEndpoint = function (s) {
	s_parts = s.split(':');

	return {
		'host': s_parts[0],
		'port': parseInt s_parts[1]
	};
}
