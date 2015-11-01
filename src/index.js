var net  = require('net'),
    conn = require('./connection');

var endpoint = {
    'host': '127.0.0.1',
    'port': 6810
};

function onConnect(sock, sockEndpoint) {
    console.log('Hello, world! I am the `onConnect` callback!');
}

function onData(sock, data) {
    console.log('Hello, world! I am the `onData` callback!');
}

conn(endpoint, onConnect, onData);
