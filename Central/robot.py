
import cv2
import numpy as np
from object import Object
from utils import *
from params import *
import math
class Robot(Object):

	def __init__(self,iD):
		
		Object.__init__(self)
		self.id = iD		
		self.angle = 0
		self.oldAngle = 0


	def drawRobot(self, frame):

		x = self.get_img_x()
		y = self.get_img_y()
		angle = self.getAngle()

		real_x = self.get_x_pos()
		realy_y = self.get_y_pos()

		cv2.circle(frame, (x,y), 10,(0,0,255),1)
		cv2.putText(frame, str((x,y)), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, 4)
		cv2.putText(frame, 'Robot', (x + 17,y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,4)
		cv2.putText(frame, 'iD ' + str(self.id), (x + 17,y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,4)
		cv2.putText(frame, 'Angle ' + str(self.angle), (x + 17,y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1,4)
		cv2.imwrite('ROBOT1.jpg', frame)


	def calibrateRobot(self,capture):

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

			self.trackFilteredRobot(threshold, frameHSV, frame)
			
			cv2.imshow(windowName2, threshold)
			cv2.imshow(windowName, frame)

			cv2.imwrite('ThresholdHSV.jpg',threshold)
			k = cv2.waitKey(5) & 0xFF
			if k == ord('q'):
				self.setHSVlower(lower)
				self.setHSVupper(upper)

				print 'ROBOT HSV VALUES SET'
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
	
	def trackFilteredRobot(self, threshold, frameHSV, frame):

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



		if(len(filteredContours) == 2):
			if(cv2.contourArea(filteredContours[0]) < cv2.contourArea(filteredContours[1])):
				c1 = 1
				c2 = 0
			else:
				c1 = 0
				c2 = 1

			centerPoints = []
			for contour in (filteredContours):
				area = cv2.contourArea(contour)
				if(area > 50):
						M = cv2.moments(contour)
						centerPoints.append((int((M["m10"] / M["m00"])), int((M["m01"] / M["m00"]))))

			cv2.circle(frame, centerPoints[c1], 9,(0,0,255),-1,8,0)
			cv2.line(frame, centerPoints[c1], centerPoints[c2], (0,0,255), 4,8,0)

			angle = math.atan2(centerPoints[c2][1] - centerPoints[c1][1],centerPoints[c2][0] - centerPoints[c1][0] ) * 180/math.pi

			intAngle = int(angle)
			if(intAngle <= 0):
				intAngle = intAngle * (-1)
			else:
				intAngle = 360 - intAngle

			real_center_x = int((centerPoints[c1][0] + centerPoints[c2][0])/2)
			real_center_y = int((centerPoints[c1][1] + centerPoints[c2][1])/2)

			fieldposition = convertCoordinates(real_center_x,real_center_y)

			if(abs(intAngle - self.getOldAngle()) > MIN_CHANGE):
				self.setAngle(intAngle)
			if((abs(fieldposition[0] - self.get_x_pos()) > MIN_CHANGE) and (abs(fieldposition[0] - self.get_x_pos()) < MAX_CHANGE)):
				self.set_x_pos(fieldposition[0])
				self.set_img_x(int(centerPoints[c1][0]))
			if((abs(fieldposition[1] - self.get_y_pos()) > MIN_CHANGE) and (abs(fieldposition[1] - self.get_y_pos()) < MAX_CHANGE)):
				self.set_x_pos(fieldposition[1])
				self.set_img_y(int(centerPoints[c1][1]))

			self.drawRobot(frame)

	def setAngle(self, newAngle):
		self.oldAngle = self.angle
		self.angle = newAngle
	
	def getAngle(self):
		return self.angle
	

	def getOldAngle(self):
		return self.oldAngle

	def PosInfo(self):

		x = self.get_img_x()
		y = self.get_img_y()
		angle = self.getAngle()

		return tuple((x,y,angle))