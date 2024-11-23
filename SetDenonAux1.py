#!/usr/bin/env python3

import os
import time
import subprocess
import requests
import sys
from time import sleep
from enum import Enum

PLAYING = 1
OFFLINE = 2

multiRoomActive = True
debugOutput = False
currentState = OFFLINE # the current state

def isRunningHTTP():
	res = requests.get('http://servermoode/command/?cmd=get_output_format')
	if debugOutput :
		print(res.text)
	if "PCM" in res.text:
		return True 
	else: 
		return False

def isRunningLocal():
	if debugOutput :
		#print  (os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()   )
		print (os.popen('sudo moodeutl -d -gv rxactive').read())
    	#will return True if "Running" is found in any sound card.
	if "1" in os.popen('sudo moodeutl -d -gv rxactive').read():
		#print ("rx active")
		return True
	else:
		#print ("rx inactive")
		return False

def isRunningSoundcard():
	if debugOutput :
		print  (os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()   )
    	#will return True if "Running" is found in any sound card.
	return "RUNNING" in os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()
	


def isRunning(): 
	if isRunningLocal():
		#print("local on")
		if multiRoomActive:
			if isRunningHTTP():
				#print("HTTP true")					
				return True
			else:
				#print("HTTP false")
				return False
		else:
				#print("multiroom off ")
				return True
	else:
		#print("local off")
		return False

	
while True:
	try:
		status = isRunning()
	
		if status == True and currentState == OFFLINE :  
			try:  
				subprocess.call(['expect', '/home/moode/DenonService/SetDenonAux1.sh'])
			except:
				print("telnet problem") 
			#workaround for HDMI issue: restart RX client
			if isRunningSoundcard() == False:
				print("restarting trx-rx")
				os.popen('sudo killall trx-rx').read()
				sleep(1)
				try:
					os.popen('sudo trx-rx -d default:vc4hdmi0 -h 239.0.0.1 -p 1350 -m 128 -j 64 -f 960 -R 45 -D /tmp/trx-rxpid ')
				except:
					print("trx-rx error")
				sleep(2)
			currentState = PLAYING 
			print("Denon set to aux1")
		
		elif status == False and currentState == PLAYING : 
			currentState = OFFLINE 
			print("stopped, dont change Denon CH")    
                                 
		else:
			pass
			if debugOutput :
				print("No State Change...")
		sleep(0.5)
	except KeyboardInterrupt:
		sys.exit(0)
	except:
		status = False
		print("httping not possible")
	
