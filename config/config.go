/*
Package config contains utilities for dealing with configuration data.
*/
package config

type AccessList struct {
	addresses []string
	domains   []string
	owners    []string
}

type Endpoint struct {
	hostname string
	port     uint16
}

type Config struct {
	blacklist         AccessList
	debug             bool
	host              Endpoint
	pingInterval      uint
	registeredDomains []string
}
