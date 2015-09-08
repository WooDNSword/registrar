# WooDNSword Registrar Protocol

## Message format
All messages are sent as JSON, terminated by a newline character `\n`, or ASCII
character code `0x0A`. For example:

	Message: '{ "type": "foo" }\n'

**Worth noting is that the ASCII character represented by the hex code
`0x0A` takes the place of the aforementioned placeholder `\n`.**

---

In the case of lengthy messages, the messages will be
chunked into multiple different messages, like so:

    Message 1: '{ "type": "fo'
    Message 2: 'o" }\n'

...which properly received and concatenated would result in:

    Message: '{ "type": "foo" }'

---

It sometimes may be the case that multiple messages are sent at once,
delimited by newline characters, as shown:

    Message 1: '{ "type": "fo'
    Message 2: 'o" }\n{ "type": "bar" '
    Message 3: '}\n'

In this case, simply split on newlines, resulting in that which follows:

	Message 1: '{ "type": "foo" }'
	Message 2: '{ "type": "bar" }'
