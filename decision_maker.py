"""
 @ author: rhagan21, tgeither
 date: 03/11/17
"""

#!/usr/bin/python

#import rospy
#from std_msgs.msg import String
import time
from multiwii import MultiWii
from autoscripts import takeoff
from autoscripts import land
import serial

mw = MultiWii('/dev/ttyUSB0') # pass in the port to create a new multiwii object
ser=serial.Serial()

# NOTES:
# IMMEDIATE GOAL: Startup scripts and X/Y adjustments
# QUESTION: What does "Naze sensors good" mean?
# Call with python2.7 (on rachel's computer: use python2 in /usr/bin/python2)

# These vars haven't been set yet but they will be used to tell the drone what state to go into
#shutdown_state:
#define ACTIVE = 1
#define PREPARE_TO_SHUTDOWN = 2
#define SHUTDOWN = 3

#main_state:
#define PREFLIGHT_CHECKS = 1
#define TAKEOFF = 2
#define TRACKING_TARGET = 3
#define RELOCATING_TARGET = 4

################
# PRE TAKE OFF #
################

#shutdown_state = 1
#main_state = 1

#IGNORE FOR NOW:
# Is battery low?
    # If yes, low volt buzz, flash red light, shut down (shutdown_state = 2 then 3)
    # If no, continue

#Chris sez: you can get gyroscope info thru a command. Google MultiWii Serial Protocol
#It looks like we'll want to use MSP_RAW_IMU and then mess with the output until we figure out exactly what its outputting. This function supposedly just returns unitless numbers  
# http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol
gyro_signal = mw.askRC() #askRC from multiwii.py has roll and pitch in 0th and 1st positions
roll = gyro_signal[0]
pitch = gyro_signal[1]

print("Roll: ", roll, "Pitch: ", pitch)
# TODO: Using arbitrary values
while( roll < 1000 or roll > 2000 or pitch < 1000 or pitch > 2000 ):
    print("Gyro returned a bad roll (", roll, ") or pitch (", pitch, "), Give bad status buzz, wait 3 seconds and shut off")
    # give "bad status" buzz
    # wait 3 seconds 
    timeout = time.time() + 3

# Wait 6 seconds, give "ready set go" buzz
print("Passed gyro test, give ready set go buzz, wait six seconds and enter takeoff procedure")
timeout = time.time() + 6

#Takeoff procedure
print("Enter takeoff procedure")
# Set to hover mode (Use the takeoff(mw) function in autoscripts.py)
# takeoff(self)
# go straight up
# find person

#################
# POST TAKE OFF #
#################

#off_signal = 1
# Off signal detected
#if(off_signal):
    # Yes: Shut down (autoscripts.land(mw))
    #print("Off signal detected, shut down")
    # No: Continue

# Battery low?
#low_battery_signal = 1
#if(low_battery_signal):
    # Yes: Low volt buzz, flash red light, shut down (autoscripts.land(mw))
    #print("Low battery detected, give low volt buzz, flash red light, and shut down")
    # No: Continue

#right_side_up = 1
#naze_sensors_good = 1
# Right side up, Naze sensors good?
    # No: "Bad status" buzz, shut down (autoscripts.land(mw))
    # Yes: Continue

#have_target = 1
#position = 1
#if(!(have target && position == true)):
# Have target and position == true?
    #print("Do not have target or position != true; enter relocation loop")
    # No: Relocation loop
        # Can't find: Shut down (autoscripts.land(mw))
        # If found it, return to have target and position == true
   # If yes, continue

# Check where in frame target is
# Update that position, current position, last velocity and current velocity

# Region of interest triggers bounded lines?
    # No: Return to beginning of post take off loop
    # Yes: Continue

# PID calculation
# Send movement to Naze
# Return to beginning of post take off loop
