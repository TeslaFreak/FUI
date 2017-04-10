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
	print 'beginning takeoff sequence'
	throttle = 1250
	data = [1500, 1500, 1500, throttle, 1000, 0, 0 ,0] #set all values to balanced, mode to angle, and throttle to spinning but no lifting off the ground.
	mw.getData(mw.RAW_IMU)
	floorMagZ = mw.rawIMU['mz']
	droneMagZ = floorMagZ
	print('floor:', floorMagZ, ' drone:', droneMagZ)
	desiredHeight = 50 #about a foot off the ground is 50 of this arbitrary unit
	mw.sendCMD(16, mw.SET_RAW_RC, data)
	timeout = time.time() + 8
	while droneMagZ > floorMagZ - desiredHeight:
		if time.time() > timeout:
			print 'timeout reached'
			break
		throttle = throttle + 50
		if throttle > 1850:
			throttle = 1850
		mw.setThrottle(throttle)
		mw.getData(mw.RAW_IMU)
		droneMagZ = mw.rawIMU['mz']
		print('drone magz' ,droneMagZ, ' throttle:', throttle)
		time.sleep(0.5)
		
	mw.setAux(1,2000) #turn baro mode on to begin autohovering at current height.
	mw.setThrottle(1500)
	mw.getData(mw.RC)
	print 'takeoff sequence complete'
		  
		  
#Arg: instance of multiwii object.
#Return: NA.
#Function: Runs script to tell multiwii to stop and safely land on the ground.
def land(mw):
	print 'beginning landing sequence'
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
		time.sleep(1)
	print 'landing sequence complete'
		
	
    


    
        
