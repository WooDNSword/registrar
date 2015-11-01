var assert   = require('assert'),
    connUtil = require('../../dist/connection/util');

describe('connection/util', function () {
    describe('.endpointToString', function () {
        it('should produce correct output', function (done) {
            assert.equal(
                connUtil.endpointToString({
                    'host': '127.0.0.1',
                    'port': 8080
                }),
                '127.0.0.1:8080'
            );

            assert.equal(
                connUtil.endpointToString({
                    'host': 'localhost',
                    'port': 6667
                }),
                'localhost:6667'
            );

            return done();
        });
    });

    describe('.stringToEndpoint', function () {
        it('should produce a valid endpoint object', function (done) {
            assert.deepEqual(
                {
                    'host': '127.0.0.1',
                    'port': 8080
                },
                connUtil.stringToEndpoint('localhost:6667')
            );

            assert.deepEqual(
                {
                    'host': 'localhost',
                    'port': 6667
                },
                connUtil.stringToEndpoint('localhost:6667')
            );

            return done();
        });

        it('should produce NaN when an invalid port number is provided', function (done) {
            assert.ok(
                isNaN(
                    connUtil.stringToEndpoint('127.0.0.1:invalidPort').port
                )
            );

            return done();
        });
    });
});
