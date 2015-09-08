net  = require 'net'
conn = require './connection'

HOST = '127.0.0.1'
PORT = 6810

server = do net.createServer

server.on 'connection', (sock) ->
    console.log 'CONNECTED: ' +
        conn.endpointToString sock.remoteAddress, sock.remotePort

    sock.on 'data', (data) ->
        console.log 'DATA ' + sock.remoteAddress + ': ' + data
        sock.write 'You said, "' + data + '"'
    
    sock.on 'close', (data) ->
        console.log 'CLOSED: ' + sock.remoteAddress + ':' + sock.remotePort

server.listen PORT, HOST
console.log 'Registrar listening on ' + conn.endpointToString HOST, PORT
