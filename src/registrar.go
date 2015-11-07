package registrar

import (
	"fmt"
	"net"
)

func handleConnection(conn net.Conn) {
	conn.Write([]byte("Hello, client!"))
	conn.Close()
}

func main() {
	port := "55555"

	ln, err := net.Listen("tcp", ":"+port)
	if err != nil {
		// Handle error
	}
	fmt.Println("Listening on port", port)
	for {
		conn, err := ln.Accept()
		if err != nil {
			// Handle error
		}
		go handleConnection(conn)
	}
}
