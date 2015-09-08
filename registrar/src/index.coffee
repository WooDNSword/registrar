net = require 'net'

HOST = '127.0.0.1'
PORT = 6810

endpointToString = (host, port) ->
    # Accept a hostname and a port, then concatenate them together in that
    # order, joined by a colon.
    # For example, `endpointToString '127.0.0.1', 8080` will return the string
    # '127.0.0.1:8080'.
    host + ':' + port

server = do net.createServer

server.on 'connection', (sock) ->
    console.log 'CONNECTED: ' + sock.remoteAddress + ':' + sock.remotePort

    sock.on 'data', (data) ->
        console.log 'DATA ' + sock.remoteAddress + ': ' + data
        sock.write 'You said, "' + data + '"'
    
    sock.on 'close', (data) ->
        console.log 'CLOSED: ' + sock.remoteAddress + ':' + sock.remotePort

server.listen PORT, HOST
console.log 'Registrar listening on ' + endpointToString HOST, PORT
