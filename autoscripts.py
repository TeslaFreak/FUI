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
	data = [1500, 1500, 1500, 1250, 1000, 0, 0 ,0] #set all values to balanced, mode to angle, and throttle to spinning but no lifting off the ground.
	mw.sendCMD(16, mw.SET_RAW_RC, data)
	timeout = time.time() + 2
	while True:
		if time.time() > timeout:
			break
		mw.setThrottle(1500)
		mw.getData(mw.RC)
		
	mw.setAux(1,2000) #turn baro mode on to begin autohovering at current height.
	mw.getData(mw.RC)
		  
		  
#Arg: instance of multiwii object.
#Return: NA.
#Function: Runs script to tell multiwii to stop and safely land on the ground.
def land(mw):
	mw.getData(mw.RC)
	throttle = mw.rcChannels['throttle'] #get current throttle
	data = [1500, 1500, 1500, throttle, 1000, 0, 0 ,0] #set all values to balanced, turn off baro mode, and throttle to stable hover.
	mw.sendCMD(16, mw.SET_RAW_RC, data)
	while throttle > 1000:
		throttle = throttle - 25
		if throttle < 1000:
			throttle = 1000
		mw.setThrottle(throttle)
		mw.getData(mw.RC)
		time.sleep(0.5)
		
	
    


    
        