var
    assert    = require('assert'),
    conn_util = require('../dist/connection/util');

describe('connection/util', function () {
    describe('.endpointToString', function () {
        it('should produce correct output', function (done) {
            assert.equal(
                conn_util.endpointToString({
                    host: '127.0.0.1',
                    port: 8080
                }),
                '127.0.0.1:8080'
            );

            assert.equal(
                conn_util.endpointToString({
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
                conn_util.stringToEndpoint(
                    '127.0.0.1:8080'
                ),
                {
                    host: '127.0.0.1',
                    port: 8080
                }
            );

            assert.deepEqual(
                conn_util.stringToEndpoint(
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
                isNaN(conn_util.stringToEndpoint('127.0.0.1:invalidPort').port)
            );

            done();
        });
    });
});
