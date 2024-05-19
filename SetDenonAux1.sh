#!/usr/bin/expect
spawn telnet 192.168.178.21 23
  sleep 1
  send PW?\r
  expect {
  	PWSTANDBY {send PWON\r; sleep 8}
	  PWON	    {sleep 1}
  }
  send SIAUX1\r:
  send ^]
