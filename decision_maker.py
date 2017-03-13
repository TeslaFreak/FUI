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

def enum(**enums):
    return type('Enum', (), enums)
def printstates():
    print("Shutdown state: " )
    return

# rachel : use /dev/tty/USB0
mw = MultiWii('/dev/ttyUSB0') # pass in the port to create a new multiwii object

# NOTES:
# IMMEDIATE GOAL: Startup scripts and X/Y adjustments
# QUESTION: What does "Naze sensors good" mean?
# Call with python2.7 (on rachel's computer: use python2 in /usr/bin/python2)
# TODO Check if Pi has buzzer

shutdown_state = enum(ACTIVE=1, PREPARE_TO_SHUTDOWN=2, SHUTDOWN=3)
main_state = enum(PREFLIGHT_CHECKS=1, TAKEOFF=2, TRACKING_TARGET=3, RELOCATING_TARGET=4)

################
# PRE TAKE OFF #
################

#rospy.set_param('shutdown_state', 'shutdown_state.ACTIVE')
#rospy.set_param('main_state', 'main_state.PREFLIGHT_CHECKS')

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
# TODO: Using arbitrary values, need to test to see what boundaries are acceptable
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
#rospy.set_param('main_state', 'main_state.TAKEOFF')
# Set to hover mode (Use the takeoff(mw) function in autoscripts.py)
# takeoff(self)
# go straight up
curr_main_state = main_state.TRACKING_TARGET
# find person

#################
# POST TAKE OFF #
#################

#off_signal = 1
# Off signal detected
#if(off_signal):
    # print("Off signal detected, shut down")
    # rospy.set_param('shutdown_state', 'main_state.PREPARE_TO_SHUTDOWN')
    # rospy.set_param('shutdown_state', 'main_state.SHUTDOWN')
    # autoscripts.land(mw)

#IGNORE FOR NOW
# Battery low?
#low_battery_signal = 1
#if(low_battery_signal):
    # Yes: Low volt buzz, flash red light
    # print("Low battery detected, give low volt buzz, flash red light, and shut down")
    # rospy.set_param('shutdown_state', 'main_state.PREPARE_TO_SHUTDOWN')
    # rospy.set_param('shutdown_state', 'main_state.SHUTDOWN')
    # autoscripts.land(mw)

# Assuming checking roll & pitch will be sufficient to know if the drone is right side up, we can use the same code from earlier
gyro_signal = mw.askRC()
roll = gyro_signal[0]
pitch = gyro_signal[1]
# TODO: Any other Naze sensors to check here? Need to calibrate boundaries
print("Roll: ", roll, "Pitch: ", pitch)
if( roll < 1000 or roll > 2000 or pitch < 1000 or pitch > 2000 ):
    print("Drone is not right side up, powering down")
    # rospy.set_param('shutdown_state', 'main_state.PREPARE_TO_SHUTDOWN')
    # rospy.set_param('shutdown_state', 'main_state.SHUTDOWN')
    # autoscripts.land(mw)

# DEPENDENT ON VISUAL ANALYZER ALGORITHM
# rospy.set_param('main_state', 'main_state.TRACKING_TARGET')
#have_target = 1 #from visual analyzer
#position = 1 #from visual analyzer
#if(!(have target && position == true)):
# Have target and position == true?
    # print("Do not have target or position != true; enter relocation loop")
    # rospy.set_param('main_state', 'main_state.RELOCATING_TARGET')
    # No: Relocation loop
        # Can't find: Shut down (autoscripts.land(mw))
        # rospy.set_param('shutdown_state', 'main_state.PREPARE_TO_SHUTDOWN')
        # rospy.set_param('shutdown_state', 'main_state.SHUTDOWN')
        # If found it, return to have target and position == true
   # If yes, continue

# rospy.set_param('main_state', 'main_state.TRACKING_TARGET')
# Check where in frame target is
# Update that position, current position, last velocity and current velocity

# Region of interest triggers bounded lines?
    # No: Return to beginning of post take off loop
    # Yes: Continue

# PID calculation
# Send movement to Naze
# Return to beginning of post take off loop
