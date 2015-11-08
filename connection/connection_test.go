package connection

import (
	"net"
	"testing"
)

// TestHandleConnectionClose determines whether the call to net.Conn.Close() at
// the end of HandleConnection performs successfully.
func TestHandleConnectionClose(t *testing.T) {
	// Create a net.Conn object for testing purposes.
	conn, _ := net.Pipe()

	// Pass the net.Conn object through an empty function to isolate the
	// functionality of HandleConnection. Store the return value (an error
	// object) from HandleConnection in the variable `err`.
	err := HandleConnection(func(net.Conn) {}, conn)
	if err != nil {
		t.Error(err)
	}
}
