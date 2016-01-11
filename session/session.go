// Package session provides utilities for dealing with sessions with client
// connections.
package session

import (
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
		switch initialMsg.Content[0] {
		case "registrant":
			// TODO: React and respond appropriately. This is only a
			// placeholder response.
			connection.Message{
				Type: "STATUS",
				Content: []string{"10001"},
			}.Send(conn)
		case "resolver":
			// TODO: React and respond appropriately. This is only a
			// placeholder response.
			connection.Message{
				Type: "STATUS",
				Content: []string{"20001"},
			}.Send(conn)
		default:
			// Client type not recognized.
			connection.Message{
				Type: "STATUS",
				Content: []string{"50001"},
			}.Send(conn)
		}
	} else {
		// TODO: Respond with the appropriate STATUS message.
		connection.Message{
			Type: "STATUS",
			Content: []string{"50000"},
		}.Send(conn)
	}
}
