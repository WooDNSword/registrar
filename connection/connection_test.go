package connection

import (
	"net"
	"testing"
)

// TestHandleConnection determines whether HandleConnection can accept a valid
// connectionHandler function and call it with the results expected from the
// design of the connectionHandler function.
func TestHandleConnection(t *testing.T) {
	// Create two connected net.Conn objects for testing purposes.
	connA, connB := net.Pipe()

	defer connB.Close()

	connectionHandler := func(conn net.Conn) {
		// Define a byte array to send over the connection.
		msg := []byte("Salutations!")
		// Define a byte array of empty bytes, the same length as `msg`.
		buf := make([]byte, len(msg))

		// Asynchronously write `msg` to the `conn` connection.
		go conn.Write(msg)
		// Block and read from the `connB` connection into the `buf` byte array.
		connB.Read(buf)

		/*
			Compare `buf` and `msg`.

			Note: `[]byte` objects cannot be compared, so they must be converted
			to `string` objects first.
		*/
		if string(buf) != string(msg) {
			t.Error("Message failed to transmit.")
		}
	}

	// Run the test.
	HandleConnection(connectionHandler, connA)
}

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
