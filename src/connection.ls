net = require 'net'
conn-util = require './connection/util'

module.exports = (endpoint, on-connect, on-data) ->
    server = net.create-server!

    server.on \connection, (sock) ->
        sock-endpoint =
            host: sock.remote-address
            port: sock.remote-port

        console.log 'CONNECTED: ' + conn-util.endpoint-to-string sock-endpoint

        on-connect(sock, sock-endpoint)

        sock.on \data, on-data

        sock.on \close, (data) ->
            console.log 'CLOSED: ' + conn-util.endpoint-to-string sock-endpoint
            sock.destroy!

        sock.on \error, (err) ->
            console.log err.stack
            sock.destroy!

    server.listen endpoint.port, endpoint.host
    console.log 'LISTENING: ' + conn-util.endpoint-to-string endpoint
