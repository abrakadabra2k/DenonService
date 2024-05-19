#!/usr/bin/env python3

import os
import time
import subprocess

currentState = False # the current state

def isRunning():
    return "RUNNING" in os.popen('cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING').read().split()

while True:
    if isRunning() and not currentState:         
        subprocess.call(['expect', '/home/moode/SetDenonAux1.sh']) 
        currentState = True
        print("Denon set to aux1")
        
    elif not isRunning() and currentState:   
        # switch again on playback resume to account for track changes
       
                
        if isRunning():
            # set the channel on resume, too
            print("Playback resumed, change Denon CH")
            subprocess.call(['expect', '/var/local/www/commandw/SetDenonAux1.sh']) 
            continue
        else:            
            currentState = False
            print("stopped, dont change Denon CH")    
                                 
   # else:
       # print("No State Change...")