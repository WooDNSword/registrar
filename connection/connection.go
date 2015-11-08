// Package connection provides utilities for establishing and handling
// connections and other networking artifacts.
package connection

import (
	"fmt"
	"net"
)

// Initiate creates a listener on the specified `port` and begins a loop
// spawning off instances of the supplied function `connectionHandler` for
// each connection established by the listener.
func Initiate(port string, connectionHandler func(net.Conn)) {
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Println("Oops! Could not listen on port", port, "-", err)
		return
	}
	fmt.Println("Listening on port", port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Oops! Connection attempted but could not be accepted")
			continue
		}
		go connectionHandler(conn)
	}
}
