#!/usr/bin/expect
spawn telnet 192.168.178.21 23
  sleep 1
  send PWON\r
  sleep 1
  send SIAUX1\r:
  send ^]
