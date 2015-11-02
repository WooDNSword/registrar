/**
 * Accept a hostname and a port, then construct from them an endpoint object,
 * and return the result.
 */
exports.endpoint = function (host, port) {
	return {
		'host': host,
		'port': port
	};
};

/**
 * Accept an endpoint, then concatenate its hostname and port together in that
 * order, conjoined by a colon (':'), and return the result.
 * 
 * For example, `endpointToString('127.0.0.1', 8080)` will return the string
 * '127.0.0.1:8080'.
 */
exports.endpointToString = function (endpoint) {
	return endpoint.host + ':' + endpoint.port.toString();
};

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
};
