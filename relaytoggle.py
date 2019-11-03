#!/usr/bin/env python3

import RPi.GPIO as GPIO
import os
import time

defaultDelay = 5 #seconds 
relayPin = 2 # GPIO pin in BCM
currentState = False # the current state

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

def isRunning():
    return "RUNNING" in os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()

while True:
    if isRunning() and not currentState:         
        GPIO.output(relayPin, 1)
        currentState = True
        print("Relay Activated")
        time.sleep(defaultDelay)
        
    elif not isRunning() and currentState:   
        # delay again on playback stops to account for track changes
        time.sleep(defaultDelay)
                
        if isRunning():
            # if it's running don't deactivate the realay   
            print("Playback resumed, cancelling deactivation")
            continue
        else:
            # deactivate the relay
            GPIO.output(relayPin, 0)
            currentState = False
            print("Relay Deactivated")                                     
            
        time.sleep(defaultDelay)
    else:
        print("No State Change...")
        time.sleep(defaultDelay)        