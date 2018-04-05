#UTILS FILE

import cv2
from params import *
import numpy as np

def on_trackbar(x):
	pass

def createHSVTrackbars():

	cv2.namedWindow(trackbarWindowName)

	cv2.createTrackbar('H_MIN', trackbarWindowName, H_MIN, H_MAX, on_trackbar)
	cv2.createTrackbar('H_MAX', trackbarWindowName, H_MAX, H_MAX, on_trackbar)
	cv2.createTrackbar('S_MIN', trackbarWindowName, S_MIN, S_MAX, on_trackbar)
	cv2.createTrackbar('S_MAX', trackbarWindowName, S_MAX, S_MAX, on_trackbar)
	cv2.createTrackbar('V_MIN', trackbarWindowName, V_MIN, V_MAX, on_trackbar)
	cv2.createTrackbar('V_MAX', trackbarWindowName, V_MAX, V_MAX, on_trackbar)

def convertCoordinates(x,y):

	field_x = x - field_width/2
	field_y = field_height/2 - y

	return (field_x,field_y)

def morphOps(threshold):


	erodeElement = np.ones((2,2),np.uint8)
	dilateElement = np.ones((5,5),np.uint8)

	threshold = cv2.erode(threshold,erodeElement)
	threshold = cv2.dilate(threshold,erodeElement)

	erodeElement = np.ones((4,4),np.uint8)
	dilateElement = np.ones((6,6),np.uint8)

	threshold = cv2.erode(threshold,erodeElement)
	threshold = cv2.dilate(threshold,erodeElement)