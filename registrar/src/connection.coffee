exports.endpointToString = (endpoint) ->
    # Accept a hostname and a port, then concatenate them together in that
    # order, joined by a colon.
    # For example, `endpointToString '127.0.0.1', 8080` will return the string
    # '127.0.0.1:8080'.
    endpoint.host + ':' + endpoint.port
