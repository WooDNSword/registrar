// Package session provides utilities for dealing with sessions with client
// connections.
package session

import (
	"net"
)

/*
Handler accepts a client connection and operates on it; this function is used
to define how clients are handled post-connection and pre-close. A helper
function handles connection object closing, so this function should not close
the connection itself.
*/
func Handler(conn net.Conn) {
	conn.Write([]byte("Greetings, client!"))
}
