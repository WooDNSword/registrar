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
});
