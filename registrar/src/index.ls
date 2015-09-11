net = require 'net'
conn = require './connection'

endpoint =
    host: \127.0.0.1
    port: 6810

server = net.create-server!

server.on \connection, (sock) ->
    console.log 'CONNECTED: ' +
        conn.endpoint-to-string sock.remote-address, sock.remote-port

    sock.on \data, (data) ->
        console.log 'DATA ' + sock.remote-address + ': ' + data
        sock.write 'You said, "' + data + \"

    sock.on 'close', (data) ->
        console.log 'CLOSED: ' + sock.remote-address + \: + sock.remote-port

server.listen endpoint.port, endpoint.host
console.log 'Registrar listening on ' + conn.endpoint-to-string endpoint
