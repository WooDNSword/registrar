assert = require 'assert'
conn_util = require '../../dist/connection/util'

describe 'connection/util', ->
    describe '.endpointToString', ->
        it 'should produce correct output', (done) ->
            assert.equal(
                conn_util.endpointToString
                    host: '127.0.0.1'
                    port: 8080,
                '127.0.0.1:8080'
            )

            assert.equal(
                conn_util.endpointToString
                    host: 'localhost'
                    port: 6667,
                'localhost:6667'
            )

            do done

    describe '.stringToEndpoint', ->
        it 'should produce a valid endpoint object', (done) ->
            assert.deepEqual(
                conn_util.stringToEndpoint '127.0.0.1:8080'
                    host: '127.0.0.1'
                    port: 8080
            )

            assert.deepEqual(
                conn_util.stringToEndpoint 'localhost:6667'
                    host: 'localhost'
                    port: 6667
            )

            do done

        it 'should produce NaN when an invalid port number is provided', (done) ->
            assert.ok(
                isNaN (conn_util.stringToEndpoint '127.0.0.1:invalidPort').port
            )

            do done
