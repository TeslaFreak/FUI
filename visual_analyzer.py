# USAGE
# python picamera_fps_demo.py
# python picamera_fps_demo.py --display 1

# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy

#globals
NO_X = 100000
NO_Y = 100000
currX = 0
currY = 0
currW = 0
currH = 0
prevX = 0
prevY = 0
prevW = 0
prevH = 0
foundTarget = False

#parameter globals
shutdown_state = "Shutdown_State"
active = 1
prepare_to_shutdown = 2
shutdown = 3

main_state = "Main_State"
preflight = 1
takeoff = 2
tracking = 3
relocating = 4

target_position = 'Target_Position'

#finds and returns the x and y coordinates of the rectangle closest to the center of the image 
def find_master(img, rects):
	currX = NO_X
	currY = NO_Y
	for x, y, w, h in rects:
		if (abs(x-img.shape[0]/2) < abs(currX-img.shape[0]/2) and abs(y-img.shape[1]/2) < abs(currY-img.shape[0]/2)):
			currX = x
			currY = y 
			currW = w
			currH = h
			foundTarget = True
	if (len(rects) == 0):
		foundTarget = False
		
def find_target(frame):
	found,w=hog.detectMultiScale(frame)

	# check to see if the frame should be displayed to our screen
	draw_detections(frame,found)	
	cv2.imshow("Frame", frame)

	find_master(frame, found)

def update_previous():
	prevX = currX
	prevY = currY
	prevW = currW
	prevH = currH

def shutdown():	
	'''save video block of code (debuggging?)
	rospy.set_param(shutdown_state, shutdown)'''

def initial_startup():
	while foundTarget == False:
		frame = vs.read()
		find_target(frame)
		#if (time = maxTime)
			#shutdown()

def new_frame(frame):
	#crop this with 2*x and y 
	#cropped = frame[20:300, 10:230]
	#cropped = frame[found.x-found.w:found.x+2*found.w, found.y-found.h: found.y+2*found.h]
	return frame	

#example of how to get rectangle dimensions 
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

#draws the rectangle with padding 
def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
vs.camera.vflip = True
vs.camera
time.sleep(2.0)

#utilizes HOG descriptor/person detector 
hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

initial_startup()

#DM = rospy.Publisher(target_position, tuples, queue_size=1)

# loop over some frames...this time using the threaded stream
while True:
	#check shutdown
	'''if (rospy.get_param(shutdown_state) == prepare_to_shutdown):
		shutdown()'''

	#read the frame
	frame = vs.read()
	
	#send the position values to the DM	
	#DM.publish((currX,currY,currW,currH))	

	#crop and resize the frame
	newFrame = new_frame(frame)

	# check to see if the frame should be displayed to our screen
	draw_detections(frame,found) 
	
	#update the previous variables
	update_previous()

	find_target(newFrame)
	if (foundTarget == False):
		#findtarget with bigger/original frame 		
		find_target(frame)
		if (foundTarget == False):
			#rospy.set_param(main_state, relocating)
			while foundTarget == False:
				#check shutdown
				'''if (rospy.get_param(shutdown_state) == prepare_to_shutdown):
					shutdown()'''

				#read the frame
				frame = vs.read()

				#find_target off frame
				find_target(frame)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
