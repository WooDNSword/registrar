// Package main implements the WooDNSword Registrar program.
package main

import (
	"fmt"
	"github.com/WooDNSword/registrar/config"
	"net"
)

func HandleConnection(conn net.Conn) {
	conn.Write([]byte("Hello, client!"))
	conn.Close()
}

func main() {
	cfg := config.Load("res/json/registrar.json")
	port := cfg.Host.Port

	ln, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Oops! Could not listen on port", port)
		return
	}
	fmt.Println("Listening on port", port)

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("Connection attempted but could not be accepted")
			continue
		}
		go HandleConnection(conn)
	}
}
