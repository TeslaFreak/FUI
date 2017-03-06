import serial #reading serial data from bluetooth
import rospy #ros for topics
btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=0.5)

# the set of acceptable strings for shuting down.
SHUTDOWN_STRING = "off"
    
while True:
    rcv = btSerial.read(512)
    if rcv:
        if rcv = SHUTDOWN_STRING:
            #send shutdown command
            rospy.set_param('Shutdown_State',-2)
            btSerial.write("Shutting down!\n") #should send string to sending "app" untested
            
        #log bluetooth command to log file ROS_ROOT/log or ~/.ros/log
        rorpy.loginfo("Bluetooth command recieved: %s", rsv)