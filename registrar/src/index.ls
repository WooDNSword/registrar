net = require 'net'
conn = require './connection'

endpoint =
    host: \127.0.0.1
    port: 6810

on-connect = (sock, sock-endpoint) ->
    console.log 'Hello, world! I am the `on-connect` callback!'

on-data = (sock, data) ->
    console.log 'Hello, world! I am the `on-data` callback!'

conn endpoint, on-connect, on-data
