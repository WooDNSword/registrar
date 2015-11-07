// Package config contains utilities for dealing with configuration data.
package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type AccessList struct {
	Addresses, Domains, Owners []string
}

type Endpoint struct {
	Hostname, Port string
}

type Config struct {
	Blacklist         AccessList
	Debug             bool
	Host              Endpoint
	PingInterval      uint
	RegisteredDomains []string
}

// Load accepts a path to a configuration file and serializes it, returning
// the resulting struct with type Config.
func Load(path string) Config {
	var cfg Config

	cfgFile, err := os.Open(path)
	if err != nil {
		fmt.Println(err)
		return cfg
	}
	defer cfgFile.Close()

	dec := json.NewDecoder(cfgFile)
	dec.Decode(&cfg)

	return cfg
}
