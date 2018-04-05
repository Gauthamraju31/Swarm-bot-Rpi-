

import cv2
import numpy as np
from object import Object
from utils import *
from params import *
import math


class Victim(Object):

	def __init__(self):

		Object.__init__(self)
		self.position = []

	def findVictim(self, capture):

		self.setHSVlower([78,103,97])
		lower = self.getHSVlower()
		self.setHSVupper([114,235,187])
		upper = self.getHSVupper()
		

		createHSVTrackbars()
		cv2.setTrackbarPos('H_MIN', trackbarWindowName, lower[0])
		cv2.setTrackbarPos('H_MAX', trackbarWindowName, upper[0])
		cv2.setTrackbarPos('S_MIN', trackbarWindowName, lower[1])
		cv2.setTrackbarPos('S_MAX', trackbarWindowName, upper[1])
		cv2.setTrackbarPos('V_MIN', trackbarWindowName, lower[2])
		cv2.setTrackbarPos('V_MAX', trackbarWindowName, upper[2])

		while(True):
			ret, frame = capture.read()
			frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

			threshold = cv2.inRange(frameHSV, lower, upper)

			morphOps(threshold)

			h_min = cv2.getTrackbarPos( "H_MIN", trackbarWindowName);
			h_max = cv2.getTrackbarPos( "H_MAX", trackbarWindowName);
			s_min = cv2.getTrackbarPos( "S_MIN", trackbarWindowName);
			s_max = cv2.getTrackbarPos( "S_MAX", trackbarWindowName);
			v_min = cv2.getTrackbarPos( "V_MIN", trackbarWindowName);
			v_max = cv2.getTrackbarPos( "V_MAX", trackbarWindowName);

			lower = np.array([h_min,s_min,v_min])
			upper = np.array([h_max,s_max,v_max])

			self.setHSVlower(lower)
			self.setHSVupper(upper)

			self.trackFilteredVictim(threshold, frameHSV, frame)
			
			cv2.imshow(windowName2, threshold)
			cv2.imshow(windowName, frame)

			k = cv2.waitKey(5) & 0xFF
			if k == ord('q'):
				self.setHSVlower(lower)
				self.setHSVupper(upper)

				print 'Victim HSV VALUES SET'
				print 'h_min: ', h_min
				print 'h_max: ', h_max
				print 's_min: ', s_min
				print 's_max: ', s_max
				print 'v_min: ', v_min
				print 'v_max: ', v_max

				cv2.destroyAllWindows()

				H_MIN = 0
				H_MAX = 180
				S_MIN = 0
				S_MAX = 255
				V_MIN = 0
				V_MAX = 255

				break

	def drawVictim(self, frame):

		x = self.get_img_x()
		y = self.get_img_y()

		cv2.circle(frame, (x,y), 10,(0,0,255),1)
		cv2.putText(frame, str((x,y)), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, 4)
		cv2.putText(frame, 'Victim', (x + 17,y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,4)
		
	def trackFilteredVictim(self, threshold, frameHSV, frame):

		temp = threshold.copy()
		morphOps(threshold)
		c1 = 0
		c2 = 1

		_, contours,_ = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		
		filteredContours = []
		for contour in contours:
			area = cv2.contourArea(contour)
			if(area > 50):
				filteredContours.append(contour)
		
		cv2.drawContours(frame,filteredContours,-1,(0,255,0),1)



		if(len(filteredContours) == 1):
			
			
			for contour in (filteredContours):
				area = cv2.contourArea(contour)
				if(area > 50 and area < 500):

					M = cv2.moments(contour)
					cX = int((M["m10"] / M["m00"]))
					cY = int((M["m01"] / M["m00"]))
					self.position = list((cX,cY))
					cv2.circle(frame, aelf.position, 9,(0,0,255),-1,8,0)
					
			if(len(victimPosition) != 0):
				real_center_x = int(self.position[0])
				real_center_y = int(self.position[1])

				self.set_img_x(int(real_center_x))
				self.set_img_y(int(real_center_y))

				self.drawVictim(frame)
