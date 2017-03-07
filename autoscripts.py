# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 20:06:32 2017

@author: Chris
"""

import time

		
#Arg: instance of multiwii object.
#Return: NA.
#Function: Runs script to tell multiwii to takeoff and begin to hover.
def takeoff(mw):
	mw.rcData = [1500, 1500, 1500, 1250, 1000, 0, 0 ,0] #set all values to balanced, mode to angle, and throttle to spinning but no lifting off the ground.
	mw.setRC()
	timeout = time.time() + 2
	while True:
		if time.time() > timeout:
			break
		mw.setThrottle(1500)
		mw.askRC()
		
	mw.setAux(1,2000) #turn baro mode on to begin autohovering at current height.
	mw.askRC()
		  
		  
#Arg: instance of multiwii object.
#Return: NA.
#Function: Runs script to tell multiwii to stop and safely land on the ground.
def land(mw):
	mw.askRC()
	throttle = mw.throttle #get current throttle
	mw.rcData = [1500, 1500, 1500, throttle, 1000, 0, 0 ,0] #set all values to balanced, turn off baro mode, and throttle to stable hover.
	mw.setRC()
	while throttle > 1000:
		throttle = throttle - 25
		if throttle < 1000:
			throttle = 1000
		mw.setThrottle(throttle)
		mw.askRC()
		time.sleep(1)
		
	
    


    
        