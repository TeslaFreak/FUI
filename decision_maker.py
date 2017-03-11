#!/usr/bin/python

import rospy
from std_msgs.msg import String

#desicion maker file

################
# PRE TAKE OFF #
################

# QUESTION: Are we going to be able to check the battery from the code running on the Pi?
# Is battery low?
    # If yes, low volt buzz, flash red light, shut down
    # If no, continue

# while( gyro returns bad angle )
    # give "bad status" buzz
    # wait 3 seconds

# Wait 6 seconds, give "ready set go" buzz

#Takeoff procedure
    # Set to hover mode
    # go straight up
    # find person

#################
# POST TAKE OFF #
#################

# Off signal detected
    # Yes: Shut down
    # No: Continue

# Battery low?
    # Yes: Low volt buzz, flash red light, shut down
    # No: Continue

# Right side up, Naze sensors good?
    # No: "Bad status" buzz, shut down
    # Yes: Continue

# Have target and position == true?
    # No: Relocation loop
        # Can't find: Shut down
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
