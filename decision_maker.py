"""
 @ author: rhagan21, tgeither
 date: 03/11/17
"""

#!/usr/bin/python

import rospy
from std_msgs.msg import String
import time

# NOTES:
# QUESTION: Are we going to be able to check the battery from the code running on the Pi?
# IMMEDIATE GOAL: Startup scripts and X/Y adjustments
# QUESTION: Do startup scripts require the entire pre-take off loop?

# These vars haven't been set yet but they will be used to tell the drone what state to go into
#shutdown state
#define ACTIVE = 1
#define PREPARE_TO_SHUTDOWN = 2
#define SHUTDOWN = 3

#main state
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

# look into ROS variables

#Chris sez: you can get gyroscope info thru a command. Google MultiWii Serial Protocol
#It looks like we'll want to use MSP_RAW_IMU and then mess ith the output until we figure out exactly what its outputting. This function supposedly just returns unitless numbers  
# http://www.multiwii.com/wiki/index.php?title=Multiwii_Serial_Protocol
# We may be able to just use ask_rc
while( askRC(self)[0] is bad or askRC(self)[1] is bad ):
# while( gyro returns bad angle ) # Use ask_rc? Worried about pitch and roll
    # give "bad status" buzz
    # wait 3 seconds 
    timeout = time.time() + 2

# Wait 6 seconds, give "ready set go" buzz
timeout = time.time() + 6

#Takeoff procedure
# Set to hover mode (Use the takeoff(mw) function in autoscripts.py)
takeoff(self)
# go straight up
# find person

#################
# POST TAKE OFF #
#################

# Off signal detected
    # Yes: Shut down (autoscripts.land(mw))
    # No: Continue

# Battery low?
    # Yes: Low volt buzz, flash red light, shut down (autoscripts.land(mw))
    # No: Continue

# Right side up, Naze sensors good?
    # No: "Bad status" buzz, shut down (autoscripts.land(mw))
    # Yes: Continue

# Have target and position == true?
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
