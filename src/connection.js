var net      = require('net'),
    connUtil = require('./connection/util');

module.exports = function (endpoint, onConnect, onData) {
    var server = net.createServer();

    server.on('connection', function (sock) {
        var sockEndpoint = connUtil.endpoint(
            sock.remoteAddress,
            sock.remotePort
        );

        console.log('CONNECTED: ' + connUtil.endpointToString(sockEndpoint));

        onConnect(sock, sockEndpoint);

        sock.on('data', onData);

        sock.on('close', function (data) {
            console.log('CLOSED: ' + connUtil.endpointToString(sockEndpoint));
        });

        sock.on('error', function (err) {
            console.log(err.stack);
            sock.destroy();
        });
    });

    server.listen(endpoint.port, endpoint.host);
    console.log('LISTENING: ' + connUtil.endpointToString(endpoint));
};