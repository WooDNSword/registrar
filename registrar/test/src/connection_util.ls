assert = require 'assert'
conn-util = require '../../dist/connection/util'

describe 'connection/util', ->
    describe '.endpoint-to-string', (,) ->
        it 'should produce correct output', (done) ->
            assert.equal(
                conn-util.endpoint-to-string(
                    host: '127.0.0.1'
                    port: 8080
                ),
                '127.0.0.1:8080'
            )

            assert.equal(
                conn-util.endpoint-to-string(
                    host: 'localhost'
                    port: 6667
                ),
                'localhost:6667'
            )

            done!

    describe '.string-to-endpoint', (,) ->
        it 'should produce a valid endpoint object', (done) ->
            assert.deepEqual(
                (conn-util.string-to-endpoint '127.0.0.1:8080'),
                host: '127.0.0.1'
                port: 8080
            )

            assert.deepEqual(
                (conn-util.string-to-endpoint 'localhost:6667'),
                host: 'localhost'
                port: 6667
            )

            done!

        it 'should produce NaN when an invalid port number is provided', (done) ->
            assert.ok . isNaN <| (conn-util.string-to-endpoint '127.0.0.1:invalidPort').port

            done!
    