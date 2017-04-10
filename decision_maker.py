"""
 @ author: rhagan21, tgeither
 date: 03/11/17
"""

#!/usr/bin/python

#import rospy
#from std_msgs.msg import String
import time
from pyMultiwii import MultiWii
from autoscripts import takeoff
from autoscripts import land
from sys import stdout
from testLeftRight import turnLeft

def enum(**enums):
    return type('Enum', (), enums)
def printstates():
    print("Shutdown state: " )
    return

# rachel : use /dev/tty/USB0
mw = MultiWii('COM3') # pass in the port to create a new multiwii object

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
main_state = 1
if (main_state == 1):
     mw.getData(MultiWii.ATTITUDE)
     angleX = float(mw.attitude['angx'])
     angleY = float(mw.attitude['angy'])

     message = "angleX = {:+.2f} \t angleY = {:+.2f} \t".format(angleX, angleY)
     stdout.write("\r%s" % message )

     # TODO: Using arbitrary values, need to test to see what boundaries are acceptable
     while( angleX < -20 or angleX > 20 or angleY < -20 or angleY > 20 ):
          print("Gyro returned a bad roll (", angleX, ") or pitch (", angleY, "), Give bad status buzz, wait 3 seconds and shut off")
          # give "bad status" buzz
          # wait 3 seconds
          time.sleep(3)
          mw.getData(MultiWii.ATTITUDE)
          angleX = float(mw.attitude['angx'])
          angleY = float(mw.attitude['angy'])
          message = "angleX = {:+.2f} \t angleY = {:+.2f} \t".format(angleX, angleY)
          stdout.write("\r%s" % message )

     # Wait 6 seconds, give "ready set go" buzz
     print("Passed gyro test, give ready set go buzz, wait six seconds and enter takeoff procedure")
     time.sleep(6)

#Takeoff procedure
print("Enter takeoff procedure")
mw.arm()
#takeoff(mw)
#mw.getData(MultiWii.RC)
#throttle = float(mw.RC['throttle'])
#message = "throttle = {:+.2f} \t".format(throttle)
#stdout.write("\r%s" % message)
#turnLeft(mw)
#mw.getData(MultiWii.RC)
#throttle = float(mw.RC['throttle'])
#message = "throttle = {:+.2f} \t".format(throttle)
#stdout.write("\r%s" % message)
#land(mw)
#mw.getData(MultiWii.RC)
#throttle = float(mw.RC['throttle'])
#message = "throttle = {:+.2f} \t".format(throttle)
#stdout.write("\r%s" % message)
mw.disarm()
#rospy.set_param('main_state', 'main_state.TAKEOFF')
# Set to hover mode (Use the takeoff(mw) function in autoscripts.py)
# takeoff(self)
# go straight up
#curr_main_state = main_state.TRACKING_TARGET
# find person

#################
# POST TAKE OFF #
#################

#off_signal = False
#x = True
#while (x):
    # Off signal detected
	#Seems redundant to have this
    #if(off_signal):
         #print("Off signal detected, shut down")
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
     #mw.getData(MultiWii.ATTITUDE)
     #angleX = float(mw.attitude['angx'])
     #angleY = float(mw.attitude['angy'])
     # TODO: Any other Naze sensors to check here? Need to calibrate boundaries
     #message = "angleX = {:+.2f} \t angleY = {:+.2f} \t".format(angleX, angleY)
     #stdout.write("\r%s" % message )
     #if( angleX < -45 or angleX > 45 or angleY < -45 or angleY > 45 ):
         #print("Drone is not right side up, powering down")
         # rospy.set_param('shutdown_state', 'main_state.PREPARE_TO_SHUTDOWN')
         # rospy.set_param('shutdown_state', 'main_state.SHUTDOWN')
         # autoscripts.land(mw)

# DEPENDENT ON VISUAL ANALYZER ALGORITHM
# rospy.set_param('main_state', 'main_state.TRACKING_TARGET')
#have_target = 1 #from visual analyzer
#visual analyzer send bool on if the target is found
#position = 1 #from visual analyzer
#visual analyzer send vector??? of position of frame
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