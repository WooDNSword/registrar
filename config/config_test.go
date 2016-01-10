package config

import (
	"fmt"
	"io"
	"reflect"
	"testing"
)

// TestEval determines whether Eval produces a valid Config object from ad-hoc
// example data.
func TestEval(t *testing.T) {
	var testData string
	var testResult Config
	var expectedResult Config
	var err error

	// Define an IO pipe to send/receive data locally
	reader, writer := io.Pipe()
	defer reader.Close()
	defer writer.Close()

	// First test: Determine whether Eval() produces correct results from test
	// data.

	testData = `
		{
			"blacklist": {
				"addresses": [],
				"domains": [],
				"owners": []
			},
			"debug": true,
			"host": {
				"hostname": "localhost",
				"port": "7776"
			},
			"ping interval": 180,
			"reserved domains": [
				{
					"domain": "mywebsite.com",
					"fields": [
						{
							"name": "address",
							"value": "127.0.0.1"
						}
					]
				},
				{
					"domain": "yourwebsite.com",
					"fields": [
						{
							"name": "address",
							"value": "1.2.3.4"
						}
					]
				}
			]
		}
	`
	expectedResult = Config{
		Blacklist: AccessList{
			Addresses: []string{},
			Domains:   []string{},
			Owners:    []string{},
		},
		Debug: true,
		Host: Endpoint{
			Hostname: "localhost",
			Port:     "7776",
		},
		PingInterval: 180,
		ReservedDomains: []Registration{
			Registration{
				Domain: "mywebsite.com",
				Fields: []Field{
					Field{
						Name:  "address",
						Value: "127.0.0.1",
					},
				},
			},
			Registration{
				Domain: "yourwebsite.com",
				Fields: []Field{
					Field{
						Name:  "address",
						Value: "1.2.3.4",
					},
				},
			},
		},
	}
	go writer.Write([]byte(testData))

	testResult, err = Eval(reader)
	if err != nil {
		t.Error(err)
	}

	fmt.Printf("%+v\n\n%+v\n", testResult, expectedResult)

	if !reflect.DeepEqual(testResult, expectedResult) {
		t.Error("Test result does not equal expected result.")
	}

	// Second test: Determine whether Eval() panics when it receives invalid
	// test data.

	testData = `blah blah`
	go writer.Write([]byte(testData))

	_, err = Eval(reader)
	if err == nil {
		t.Error("Eval() did not produce an error when expected to.")
	}
}
