# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import serial
import struct
import time

ser = serial.Serial()
ser.port ='COM5'
ser.baudrate=115200
ser.bytesize=serial.EIGHTBITS
ser.parity= serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.timeout=1
header = "\x24\x4d\x3c\x00"
askRC = "\x69\x69"
askATT = "\x6C\x6C"	#MSG ID: 108
askALT = "\x6D\x6D"	#MSG ID: 109
ser.open()
rcData = [1500, 1500, 1500, 1050] #order -> roll, pitch, yaw, throttle
auxData = [1500, 1500, 1500, 1050, 1000, 1500, 2000, 1000]
timeMSP=0.02

#First, run the arm command, then call this command with the desired throttle in the first rcData declaration. it will run for 5 seconds and then turn off.
#Run disarm command when finished testing for safety purposes
def runLoop():
    rcData = [1500, 1500, 1500, 1500]
    timeout = time.time() + 5
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
        
    rcData = [1500, 1500, 1500, 1050]
    timeout = time.time() + 2
    print("turning off")
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()

def littleEndian(value):
		length = len(value)	# gets the length of the data piece
		actual = ""
		for x in range(0, length/2):	#go till you've reach the halway point
			actual += value[length-2-(2*x):length-(2*x)]	#flips all of the bytes (the last shall be first)
			x += 1
		intVal = twosComp(actual)	# sends the data to be converted from 2's compliment to int
		return intVal				# returns the integer value

	###################################################################
	# twosComp(hexValue)
	#	receives: the big endian hex value (correct format)
	#	outputs:  the decimal value of that data
	#	function: if the value is negative, swaps all bits
	#			up to but not including the rightmost 1.
	#			Else, just converts straight to decimal.
	#			(Flip all the bits left of the rightmost 1)
	#	returns:  the integer value
	###################################################################
def twosComp(hexValue):
		firstVal = int(hexValue[:1], 16)
		if firstVal >= 8:	# if first bit is 1
			bValue = bin(int(hexValue, 16))
			bValue = bValue[2:]	# removes 0b header
			newBinary = []
			length = len(bValue)
			index = bValue.rfind('1')	# find the rightmost 1
			for x in range(0, index+1):	# swap bits up to rightmost 1
				if x == index:		#if at rightmost one, just append remaining bits
					newBinary.append(bValue[index:])
				elif bValue[x:x+1] == '1':
					newBinary.append('0')
				elif bValue[x:x+1] == '0':
					newBinary.append('1')
				x += 1
			newBinary = ''.join(newBinary) 	# converts char array to string
			finalVal = -int(newBinary, 2)	# converts to decimal
			return finalVal
				
		else:		# if not a negative number, simply convert to decimal
			return int(hexValue, 16)


#UNTESTED
def land():
    rcData = [1500, 1500, 1500, 1450]
    timeout = time.time() + 2
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
        
    rcData = [1500, 1500, 1500, 1350]
    timeout = time.time() + 5
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
        
    rcData = [1500, 1500, 1500, 1300]
    timeout = time.time() + 5
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
    
#UNTESTED
def takeoff():
    rcData = [1500, 1500, 1500, 1450]
    timeout = time.time() + 2
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
        
    rcData = [1500, 1500, 1500, 1500]
    timeout = time.time() + 2
    while True:
        if time.time() > timeout:
            break
        setRC(rcData)
        time.sleep(timeMSP)
        getRC()
    
        
def setRC(data):
    sendData(16, 200, data)

def sendData(data_length, code, data):
		checksum = 0
		total_data = ['$', 'M', '<', data_length, code] + data
		for i in struct.pack('<2B%dh' % len(data), *total_data[3:len(total_data)]):
			checksum = checksum ^ ord(i)

		total_data.append(checksum)

		try:
			b = None
			b = ser.write(struct.pack('<3c2B%dhB' % len(data), *total_data))
		except Exception, ex:
			print 'send data error'
			print(ex)
		return b
    
def readATT():
    attitude = 0;
    ser.write(header+askATT)
    response=ser.readline()
    msp_hex = response.encode("hex")
    attitude = littleEndian(msp_hex[10:14])
    print("attitude: " + attitude)

def getRC():
    ser.flushInput()	# cleans out the serial port
    ser.flushOutput()
    ser.write(header+askRC)	# gets RC information
    time.sleep(timeMSP)
    response = ser.readline()
    print(response)
    printTrueRC(response)
    
    
def arm():
    timer = 0
    start = time.time()
    while timer < 0.5:
        data = [1500,1500,2000,1000]
        sendData(8,200,data)
        time.sleep(0.05)
        timer = timer + (time.time() - start)
        start =  time.time()

def disarm():
    timer = 0
    start = time.time()
    while timer < 0.5:
        data = [1500,1500,1000,1000]
        sendData(8,200,data)
        time.sleep(0.05)
        timer = timer + (time.time() - start)
        start =  time.time()
            
def printTrueRC(response):
    pitch=0
    roll=0
    yaw=0
    throttle = 0
    aux = [2,2,2,2]
    msp_hex = response.encode("hex")
    if msp_hex[10:14] == "":
        print("roll unavailable")
				
    else:
        roll = float(littleEndian(msp_hex[10:14]))
	
    if msp_hex[14:18] == "":
        print("pitch unavailable")
				
    else:
        pitch = float(littleEndian(msp_hex[14:18]))
	
    if msp_hex[18:22] == "":
        print("yaw unavailable")
				
    else:
        yaw = float(littleEndian(msp_hex[18:22]))
	
    if msp_hex[22:26] == "":
		print("throttle unavailable")
				
    else:
        throttle = float(littleEndian(msp_hex[22:26]))
        
    for i in range(0, 3):
        if msp_hex[(26+(i*4)):(30+(i*4))] == "":
    		print("aux" + i + " unavailable")
    				
        else:
            aux[i] = float(littleEndian(msp_hex[(26+(i*4)):(30+(i*4))]))
				
    print("roll: " + str(roll) + " " + "pitch: " + str(pitch) + " " + "yaw: " + str(yaw) + " " + "throttle: " + str(throttle) + " aux: " + str(aux))