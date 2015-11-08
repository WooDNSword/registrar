// Package main implements the WooDNSword Registrar program.
package main

import (
	"github.com/WooDNSword/registrar/config"
	"github.com/WooDNSword/registrar/connection"
	"github.com/WooDNSword/registrar/session"
)

func main() {
	cfg := config.Load("res/json/cfg.json")
	port := cfg.Host.Port

	connection.Initiate(port, session.Handler)
}
