// Package config contains utilities for dealing with configuration data.
// TODO: Write tests for this package.
package config

import (
	"encoding/json"
	"io"
)

type AccessList struct {
	Addresses, Domains, Owners []string
}

type Endpoint struct {
	Hostname, Port string
}

type Field struct {
	Name  string
	Value string
}

type Registration struct {
	Domain string
	Fields []Field
}

type Config struct {
	Blacklist       AccessList
	Debug           bool
	Host            Endpoint
	PingInterval    uint           `json:"ping interval"`
	ReservedDomains []Registration `json:"reserved domains"`
}

/*
Eval accepts a value of type io.Reader, tries to read all data from it, then
decodes the data from JSON to a struct `cfg` of type Config.

A tuple containing that struct value `cfg` as well as a value of type `err`,
denoting whether any issues occurred during decoding, is then returned.
*/
func Eval(reader io.Reader) (Config, error) {
	var cfg Config

	dec := json.NewDecoder(reader)
	err := dec.Decode(&cfg)

	return cfg, err
}
