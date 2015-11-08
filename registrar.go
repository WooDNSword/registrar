// Package main implements the WooDNSword Registrar program.
package main

import (
	"github.com/WooDNSword/registrar/config"
	"github.com/WooDNSword/registrar/connection"
	"net"
)

func HandleConnection(conn net.Conn) {
	conn.Write([]byte("Hello, client!"))
	conn.Close()
}

func main() {
	cfg := config.Load("res/json/cfg.json")
	port := cfg.Host.Port
	
	connection.Initiate(port, HandleConnection)
}
