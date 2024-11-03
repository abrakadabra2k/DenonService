#!/usr/bin/expect
set IPaddress 192.168.178.21

spawn ping -c 3 $IPaddress 
expect  {
  " 0%"   {puts "$IPaddress  Is Up"}
  " 100%" {puts "$IPaddress  Is Down"}
}

spawn telnet $IPaddress  23
  sleep 1
  send PW?\r
  expect {
  	PWSTANDBY {send PWON\r; sleep 8}
	  PWON	  {sleep 1}
  }
  send SIAUX1\r
  sleep 1
  send SIAUX1\r
  # Send special ^] to telnet so we can tell telnet to quit.
  send ^] 