#/!usr/bin/env python

import time
import logging
import serial
import struct		# for decoding data strings


class MultiWii:

	def __init__(self, port):

		self.started = True

		self.ATT 	= 	0 	# Ask and save the attitude of the multicopter
		self.ALT 	= 	0 	# Ask and save the altitude of the multicopter
		self.RC  	= 	1 	# Ask and save the pilot commands of the multicopter
		self.SET_RC	= 	1 	# Set rc command
		self.MOT 	= 	0 	# Ask and save the PWM of the motors that the MW is writing to the multicopter
		self.RAW 	= 	0 	# Ask and save the raw imu data of the multicopter
		self.CMD 	= 	0 	# Send commands to the MW to control it
		self.UDP 	=	0 	# Save or use UDP data (to be adjusted)
		self.ASY 	=	0 	# Use async communicacion
		self.SCK 	=	0 	# Use regular socket communication
		self.SCKSRV	=	0 	# Use socketserver communication
		self.PRINT 	= 	0 	# Print data to terminal, useful for debugging
		
		###############################
		# Communication via serial port
		###############################
		self.port = port

		self.ser=serial.Serial()
		self.ser.port=self.port
		self.ser.baudrate=115200
		self.ser.bytesize=serial.EIGHTBITS
		self.ser.parity=serial.PARITY_NONE
		self.ser.stopbits=serial.STOPBITS_ONE
		self.ser.timeout=0
		self.ser.xonxoff=False
		self.ser.rtscts=False
		self.ser.dsrdtr=False
		self.ser.writeTimeout=2

		self.timeMSP=0.02
		
		try:
			self.ser.open()

		except Exception as e:
			logging.error("Error while open serial port: " + str(e))

		###############################
		# Multiwii Serial Protocol
		# Hex value for MSP request
		##############################
		self.HEADER="\x24\x4d\x3c\x00"	#MSG Send Header (to MultiWii)
		self.MSP_IDT=self.HEADER+"\x64\x64"	#MSG ID: 100
		self.MSP_STATUS=self.HEADER+"\x65\x65"	#MSG ID: 101
		self.MSP_RAW_IMU=self.HEADER+"\x66\x66"	#MSG ID: 102
		self.MSP_SERVO=self.HEADER+"\x67\x67"	#MSG ID: 103
		self.MSP_MOTOR=self.HEADER+"\x68\x68"	#MSG ID: 104
		self.MSP_RC=self.HEADER+"\x69\x69"		#MSG ID: 105
		self.MSP_RAW_GPS=self.HEADER+"\x6A\x6A"	#MSG ID: 106
		self.MSP_ATTITUDE=self.HEADER+"\x6C\x6C"	#MSG ID: 108
		self.MSP_ALTITUDE=self.HEADER+"\x6D\x6D"	#MSG ID: 109
		self.MSP_BAT = self.HEADER+"\x6E\x6E"	#MSG ID: 110
		self.MSP_COMP_GPS=self.HEADER+"\x71\x71"	#MSG ID: 111
		self.MSP_SET_RC=self.HEADER+"\xC8\xC8"  	#MSG ID: 200
		
		self.CMD2CODE = {
			# Getter
			'MSP_IDENT':100,
			'MSP_STATUS':101,
			'MSP_RAW_IMU':102,
			'MSP_SERVO':103,
			'MSP_MOTOR':104,
			'MSP_RC':105,
			'MSP_RAW_GPS':106,
			'MSP_COMP_GPS':107,
			'MSP_ATTITUDE':108,
			'MSP_ALTITUDE':109,
			'MSP_ANALOG':110,
			'MSP_RC_TUNING':111,
			'MSP_PID':112,
			'MSP_BOX':113,
			'MSP_MISC':114,
			'MSP_MOTOR_PINS':115,
			'MSP_BOXNAMES':116,
			'MSP_PIDNAMES':117,
			'MSP_WP':118,
			'MSP_BOXIDS':119,
	
			# Setter
			'MSP_SET_RAW_RC':200,
			'MSP_SET_RAW_GPS':201,
			'MSP_SET_PID':202,
			'MSP_SET_BOX':203,
			'MSP_SET_RC_TUNING':204,
			'MSP_ACC_CALIBRATION':205,
			'MSP_MAG_CALIBRATION':206,
			'MSP_SET_MISC':207,
			'MSP_RESET_CONF':208,
			'MSP_SET_WP':209,
			'MSP_SWITCH_RC_SERIAL':210,
			'MSP_IS_SERIAL':211,
			'MSP_DEBUG':254,
		}

		###############################
		# Initialize Global Variables
		###############################
		self.latitude = 0.0
		self.longitude = 0.0
		self.altitude = -0
		self.heading = -0
		self.timestamp = -0
		self.gpsString = -0
		self.numSats = -0
		self.accuracy = -1
		self.beginFlag = 0
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		self.throttle = 0
		self.aux = [0,0,0,0]
		self.angx = 0.0
		self.angy = 0.0
		self.m1 = 0
		self.m2 = 0
		self.m3 = 0
		self.m4 = 0
		self.message = ""
		self.ax = 0
		self.ay = 0
		self.az = 0
		self.gx = 0
		self.gy = 0
		self.gz = 0
		self.magx = 0
		self.magy = 0
		self.magz = 0
		self.elapsed = 0
		self.flytime = 0
		self.numOfValues = 0
		self.precision = 3
		self.rcData = [1500, 1500, 1500, 1000,1000,1000,1000,1000] #order -> roll, pitch, yaw, throttle, aux1, aux2, aux3, aux4
	
		if self.ser.isOpen():
			print("Wait 5 sec for calibrate Multiwii")
			time.sleep(5)




	def arm(self):
		timer = 0
		start = time.time()
		while timer < 0.5:
			data = [1500,1500,2000,1000]
			self.sendData(8,200,data)
			time.sleep(0.05)
			timer = timer + (time.time() - start)
			start =  time.time()

	def disarm(self):
		timer = 0
		start = time.time()
		while timer < 0.5:
			data = [1500,1500,1000,1000]
			self.sendData(8,200,data)
			time.sleep(0.05)
			timer = timer + (time.time() - start)
			start =  time.time()
        
        
	#############################################################
	# littleEndian(value)
	#	receives: a parsed, hex data piece
	#	outputs:  the decimal value of that data
	#	function: swaps byte by byte to convert little
	#			endian to big endian
	#	function: calls 2's compliment to convert to decimal
	#	returns:  The integer value
	#############################################################
	def littleEndian(self, value):
		length = len(value)	# gets the length of the data piece
		actual = ""
		for x in range(0, length/2):	#go till you've reach the halway point
			actual += value[length-2-(2*x):length-(2*x)]	#flips all of the bytes (the last shall be first)
			x += 1
		intVal = self.twosComp(actual)	# sends the data to be converted from 2's compliment to int
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
	def twosComp(self, hexValue):
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

			

	def sendData(self, data_length, code, data):
		checksum = 0
		total_data = ['$', 'M', '<', data_length, code] + data
		for i in struct.pack('<2B%dh' % len(data), *total_data[3:len(total_data)]):
			checksum = checksum ^ ord(i)

		total_data.append(checksum)

		try:
			b = None
			b = self.ser.write(struct.pack('<3c2B%dhB' % len(data), *total_data))
		except Exception, ex:
			print('send data error')
			print(ex)
		return b


	#############################################################
	# askRC()
	#	receives: nothing
	#	outputs:  nothing
	#	function: Do everything to ask the MW for data and save it on globals 
	#	returns:  nothing
	#############################################################
	def askRC(self):
		self.ser.flushInput()	# cleans out the serial port
		self.ser.flushOutput()
		self.ser.write(self.MSP_RC)	# gets RC information
		time.sleep(self.timeMSP)
		response = self.ser.readline()
		if str(response) == "":
			print("RC data unavailable")
			return
		else:
			msp_hex = response.encode("hex")
	
			if msp_hex[10:14] == "":
				print("roll unavailable")
				
			else:
				self.roll = float(self.littleEndian(msp_hex[10:14]))
	
			if msp_hex[14:18] == "":
				print("pitch unavailable")
				
			else:
				self.pitch = float(self.littleEndian(msp_hex[14:18]))
	
			if msp_hex[18:22] == "":
				print("yaw unavailable")
				
			else:
				self.yaw = float(self.littleEndian(msp_hex[18:22]))
	
			if msp_hex[22:26] == "":
				print("throttle unavailable")
				
			else:
				self.throttle = float(self.littleEndian(msp_hex[22:26]))
				
			for i in range(0, 3):
				if msp_hex[(26+(i*4)):(30+(i*4))] == "":
					print("aux" + i + " unavailable")
    				
				else:
					self.aux[i] = float(self.littleEndian(msp_hex[(26+(i*4)):(30+(i*4))]))
			
			print("roll: " + str(self.roll) + " pitch: " + str(self.pitch) + " yaw: " + str(self.yaw) + " throttle: " + str(self.throttle)+ " aux: " + str(self.aux))

	def setRC(self):
		self.sendData(16, self.CMD2CODE["MSP_SET_RAW_RC"], self.rcData)
		time.sleep(self.timeMSP)
		#print self.rcData
	
    	