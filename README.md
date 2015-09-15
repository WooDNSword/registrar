# WooDNSword

[![Join the chat at https://gitter.im/xnil/woodnsword](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/xnil/woodnsword?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A claim-based floating domain name system

### How it works

The WooDNSword backend consists of two separate programs:

+ The **registrar** is a daemon that clients and registrants connect to, and
  handles the administration, registration, deregistration, and lookups of all
  domains. This program is meant to always be running, and ties the WooDNSword
  system together. In addition to allowing registrant-registered domains, the
  relay can itself reserve domains to reduce load and ensure uptime of a
  registered domain.

+ The **registrant** is another daemon that connects to a registrar and
  registers any number of domains with the relay. When the connection is lost or
  the registrar disconnects, all registered domains are relinquished until they
  are reclaimed.
 
 WooDNSword clients send requests to a registrar for a response containing
 certain information about a domain.

 ### What if I want to register a domain name in the traditional way?

 In order to _reserve_ a domain name by paying a recurring subscription, you
 must successfully claim the domain name using a registrant, with a special flag
 (**TODO: Specify this flag in documentation**) denoting that you wish to apply
 for that domain name's registration. The host of the registrar will approve or
 deny your application at its discretion, and during the time that the domain
 name is reserved it will act as if it were claimed normally; other registrants
 will not be able to claim it.
