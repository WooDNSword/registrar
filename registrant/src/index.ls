net = require 'net'

HOST = '127.0.0.1'
PORT = 6810

client = new net.Socket!

client.on 'close', ->
    console.log 'Connection closed'

client.on 'data', (data) ->
    console.log 'DATA: ' + data
    client.destroy!

client.connect PORT, HOST, ->
    console.log 'CONNECTED TO: ' + HOST + \: + PORT
    client.write 'Hello, world!'
