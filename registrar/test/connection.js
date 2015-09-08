var
    assert     = require('assert'),
    connection = require('../dist/connection');

describe('connection', function () {
    describe('.endpointToString', function () {
        it('should produce correct output', function (done) {
            assert.equal(
                connection.endpointToString({
                    host: '127.0.0.1',
                    port: 8080
                }),
                '127.0.0.1:8080'
            );

            assert.equal(
                connection.endpointToString({
                    host: 'localhost',
                    port: 6667
                }),
                'localhost:6667'
            );

            done();
        });
    });

    describe('.stringToEndpoint', function () {
        it('should produce a valid endpoint object', function (done) {
            assert.deepEqual(
                connection.stringToEndpoint(
                    '127.0.0.1:8080'
                ),
                {
                    host: '127.0.0.1',
                    port: 8080
                }
            );

            assert.deepEqual(
                connection.stringToEndpoint(
                    'localhost:6667'
                ),
                {
                    host: 'localhost',
                    port: 6667
                }
            );

            done();
        });

        it('should produce NaN when an invalid port number is provided', function (done) {
            assert.ok(
                isNaN(connection.stringToEndpoint('127.0.0.1:invalidPort').port)
            );

            done();
        });
    });
});
