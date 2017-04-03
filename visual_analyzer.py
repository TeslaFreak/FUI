#!/usr/bin/python

import rospy
from std_msgs.msg import String

#visual analyzer file

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

def find_Master(img, rects):
	minx = NO_X
	miny = NO_X
	for x, y, w, h in rects:
		if (abs(x-img.shape(0)/2) < abs(minx-img.shape(0)/2) and abs(y-img.shape(1)/2) < abs(miny-img.shape(0)/2)):
			minx = x
			miny = y
	return minx, miny

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

# loop over some frames...this time using the threaded stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	#cropped = frame[20:300, 10:230]
	found,w=hog.detectMultiScale(frame)
	# check to see if the frame should be displayed to our screen
	draw_detections(frame,found)
	# found x y .... 2* = cropped
	#cropped = frame[found.x-found.w:found.x+2*found.w, found.y-found.h: found.y+2*found.h]
	masterCoord = find_Master(frame, found)
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
