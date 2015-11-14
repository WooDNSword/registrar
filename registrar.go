// Package main implements the WooDNSword Registrar program.
package main

import (
	"github.com/WooDNSword/registrar/config"
	"github.com/WooDNSword/registrar/connection"
	"github.com/WooDNSword/registrar/session"
	"os"
)

func main() {
	cfgFile, err := os.Open("res/json/cfg.json")
	if err != nil {
		panic(err)
	}
	
	cfg, err := config.Eval(cfgFile)
	if err != nil {
		panic(err)
	}
	
	port := cfg.Host.Port

	connection.Initiate(port, session.Handler)
}
