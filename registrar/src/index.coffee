net  = require 'net'
conn = require './connection'

endpoint =
    host: '127.0.0.1'
    port: 6810

server = do net.createServer

server.on 'connection', (sock) ->
    console.log 'CONNECTED: ' +
        conn.endpointToString sock.remoteAddress, sock.remotePort

    sock.on 'data', (data) ->
        console.log 'DATA ' + sock.remoteAddress + ': ' + data
        sock.write 'You said, "' + data + '"'
    
    sock.on 'close', (data) ->
        console.log 'CLOSED: ' + sock.remoteAddress + ':' + sock.remotePort

server.listen endpoint.port, endpoint.host
console.log 'Registrar listening on ' + conn.endpointToString endpoint
