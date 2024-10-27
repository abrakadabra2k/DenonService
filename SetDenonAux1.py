#!/usr/bin/env python3

import os
import time
import subprocess
import requests
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
		print  (os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()   )
    #will return True if "Running" is found in any sound card.
	return "RUNNING" in os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()
	


def isRunning(): 
	if isRunningLocal():
		if multiRoomActive:
			if isRunningHTTP():
				return True
			else:
				return False
		else:
				return True
	else:
		return False
	
while True:
	status = isRunning()
	if status == True and currentState == OFFLINE :         
		subprocess.call(['expect', '/home/moode/SetDenonAux1.sh']) 
		currentState = PLAYING 
		print("Denon set to aux1")
		
	elif status == False and currentState == PLAYING : 
		currentState = OFFLINE 
		print("stopped, dont change Denon CH")    
                                 
	else:
		if debugOutput :
			print("No State Change...")
    
	sleep(0.5)