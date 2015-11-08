// Package session provides utilities for dealing with sessions with client
// connections.
package session

import (
	"net"
)

func Handler(conn net.Conn) {
	conn.Write([]byte("Greetings, client!"))
}
