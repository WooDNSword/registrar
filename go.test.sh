#!/usr/bin/env bash

# Codecov Golang bash script
# Pulled from https://github.com/codecov/example-go/blob/master/go.test.sh
# Except for the addition of this comment block, no changes were made.

set -e
echo "" > coverage.txt

for d in $(find . -maxdepth 10 -type d); do
    if ls $d/*.go &> /dev/null; then
        go test -coverprofile=profile.out -covermode=atomic $d
        if [ -f profile.out ]; then
            cat profile.out >> coverage.txt
            rm profile.out
        fi
    fi
done
