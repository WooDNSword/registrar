// Package connection provides utilities for establishing and handling
// connections and other networking artifacts.
package connection

import (
	"encoding/json"
	"fmt"
	"io"
	"net"
)

// TODO: Move Message struct type to shared repository (exists in registrant
// codebase as well).
// TODO: Document Message struct type.
type Message struct {
	Type    string
	Content []string
}

// TODO: Move Message.ByteString() to shared repository (exists in registrant
// codebase as well).
// TODO: Document Message.ByteString().
func (msg Message) ByteString() []byte {
	msgJson, err := json.Marshal(msg)
	if err != nil {
		panic(err)
	}

	return msgJson
}

// TODO: Move Message.Send() to shared repository (exists in registrant codebase
// as well).
// TODO: Document Message.Send().
func (msg Message) Send(conn net.Conn) (int, error) {
	return conn.Write(msg.ByteString())
}

// TODO: Move Recv() to shared repository (exists in registrant codebase as
// well).
// TODO: Document Recv().
func Recv(reader io.Reader) Message {
	var msg Message

	dec := json.NewDecoder(reader)
	err := dec.Decode(&msg)
	if err != nil {
		panic(err)
	}

	return msg
}

/*
HandleConnection spawns an instance of a supplied `connectionHandler`
function, which it supplies a net.Conn object `conn` to, and closes the
connection afterwards to ensure that it gets closed even if
`connectionHandler` does not close it.

An error object is returned, detailing whether the call to `.Close()` was
successful.
*/
func HandleConnection(connectionHandler func(net.Conn), conn net.Conn) error {
	connectionHandler(conn)
	return conn.Close()
}

/*
Initiate creates a listener on the specified `port` and begins a loop
spawning off instances of the supplied function `connectionHandler` with the
helper function `HandleConnection` for each connection established by the
listener.
*/
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
		go HandleConnection(connectionHandler, conn)
	}
}
