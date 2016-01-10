// Package session provides utilities for dealing with sessions with client
// connections.
package session

import (
	"fmt"
	"github.com/WooDNSword/registrar/connection"
	"net"
)

/*
Handler accepts a client connection and operates on it; this function is used
to define how clients are handled post-connection and pre-close. A helper
function handles connection object closing, so this function should not close
the connection itself.
*/
func Handler(conn net.Conn) {
	initialMsg := connection.Recv(conn)
	if initialMsg.Type == "IDENT" && len(initialMsg.Content) > 0 {
		// TODO: React to IDENT message with identification then respond with
		// the appropriate STATUS message.
		// TODO: Remove fmt.Println().
		fmt.Println(initialMsg.Content[0])
	} else {
		// TODO: Respond with the appropriate STATUS message.
		panic("There's something wrong here. This message is a placeholder.")
	}
}
