var net      = require('net'),
    conn     = require('./connection'),
    connUtil = require('./connection/util');

var endpoint = connUtil.stringToEndpoint('127.0.0.1:6810');

function onConnect(sock, sockEndpoint) {
    console.log('Hello, world! I am the `onConnect` callback!');
}

function onData(sock, data) {
    console.log('Hello, world! I am the `onData` callback!');
}

conn(endpoint, onConnect, onData);
