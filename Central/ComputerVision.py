from robot import Robot
from object import Object
from victim import Victim
from utils import *
import cv2
from params import *
import time
import networkx as nx
import matplotlib.pyplot as plt
import math




G = nx.Graph()
nodes = set()
obstacleContours = None
def calibrateField(capture):
	field_center_y = 241
	field_center_x = 262
	field_width = 506
	field_height = 435
	threshValue = 85
	field_origin_x = None
	field_origin_y = None

	cv2.namedWindow(trackbarWindowName,0)

	cv2.createTrackbar('Field Center Y', trackbarWindowName, field_center_y_min, field_center_y_max ,on_trackbar)
	cv2.createTrackbar('Field Center X', trackbarWindowName, field_center_x_min, field_center_x_max ,on_trackbar)
	cv2.createTrackbar('Field Height', trackbarWindowName, field_height_min, field_height_max ,on_trackbar)
	cv2.createTrackbar('Field Width', trackbarWindowName, field_width_min, field_width_max ,on_trackbar)

	cv2.createTrackbar('Thresh', trackbarWindowName,threshMin, threshMax ,on_trackbar)
	
	cv2.setTrackbarPos('Field Center Y', trackbarWindowName, field_center_y)
	cv2.setTrackbarPos('Field Center X', trackbarWindowName, field_center_x)
	cv2.setTrackbarPos('Field Height', trackbarWindowName, field_height)
	cv2.setTrackbarPos('Field Width', trackbarWindowName, field_width)
	cv2.setTrackbarPos('Thresh', trackbarWindowName, threshValue)

	while(True):
		ret, frame = capture.read()
		field_center_y = cv2.getTrackbarPos( "Field Center Y", trackbarWindowName)
		field_center_x = cv2.getTrackbarPos( "Field Center X", trackbarWindowName)
		field_height = cv2.getTrackbarPos( "Field Height", trackbarWindowName)
		field_width = cv2.getTrackbarPos( "Field Width", trackbarWindowName)
		threshValue = cv2.getTrackbarPos( "Thresh", trackbarWindowName)

		frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		threshold = cv2.inRange(frameGray, 0, threshValue)
		_,obContours,_ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		filteredContours = []
		for contour in obContours:
			area = cv2.contourArea(contour)
			if(area > 70 and area < 7000):
				filteredContours.append(contour)

		cv2.drawContours(frame,filteredContours,-1,(0,0,255),1)

		field_origin_x = field_center_x - (field_width/2)
		field_origin_y = field_center_y - (field_height/2)


		top_left = (field_origin_x, field_origin_y)
		bottom_right = (field_origin_x + field_width, field_origin_y + field_height )
		
		top_mid = (field_center_x,field_origin_y)
		bottom_mid = (field_center_x, field_origin_y + field_height)
		left_mid = (field_origin_x, field_center_y)
		right_mid = (field_origin_x + field_width, field_center_y)
		
		cv2.line(frame,top_mid, bottom_mid, (200,200,200), 1, 8, 0)
		cv2.line(frame,left_mid, right_mid, (200,200,200), 1, 8, 0)
		cv2.rectangle(frame,top_left, bottom_right , (0,255,0), 1, 8, 0)

		cv2.circle(frame,(field_origin_x, field_origin_y),2,(255,0,0),-1)
		
		cv2.imshow(windowName, frame)
		cv2.imwrite('Frame.jpg',frame)
		
		cv2.imshow(windowName2, threshold)
		k = cv2.waitKey(5) & 0xFF
		if k == ord('q'):
			world = np.zeros([field_height, field_width,3],dtype = np.uint8)
			world.fill(255)
			cv2.drawContours(world,filteredContours,-1,0,cv2.FILLED)
			BW = cv2.cvtColor(world, cv2.COLOR_BGR2GRAY)
			_,BW = cv2.threshold(BW, 150, 255, cv2.THRESH_BINARY)
			img = np.zeros([BW.shape[0], BW.shape[1]], np.uint8)
			x =  field_origin_x + 20
			y = field_origin_y + 20
			w = field_width - 20
			h = field_height - 20
			img[y:y+h,x:x+w] = BW[y:y+h,x:x+w]
			cv2.imwrite('Threshold.jpg', img)
			cv2.imshow('IMAGE', img)
			cv2.waitKey(0)
			navMesh(world,filteredContours, img)			
			field_center_y = cv2.getTrackbarPos( "Field Center Y", trackbarWindowName)
			field_center_x = cv2.getTrackbarPos( "Field Center X", trackbarWindowName)
			field_height = cv2.getTrackbarPos( "Field Height", trackbarWindowName)
			field_width = cv2.getTrackbarPos( "Field Width", trackbarWindowName)
			threshValue = cv2.getTrackbarPos( "Thresh", trackbarWindowName)
			print 'Field Values Saved'
			print 'Field Center Y: ', str(field_center_y)
			print 'Field Center X: ', str(field_center_x)
			print 'Field Width: ', str(field_width)
			print 'Field Height: ', str(field_height)
			print 'Thresh: ', str(threshValue)
			cv2.destroyAllWindows()
			break

def in_navigable(image, points):
	pt1 = points[0]
	pt2 = points[1]

	m12 = (int((pt1[0] + pt2[0])/2),int((pt1[1] + pt2[1])/2))
	m12_1 = (int((m12[0] + pt1[0])/2),int((m12[1] + pt1[1])/2))
	m12_2 = (int((m12[0] + pt2[0])/2),int((m12[1] + pt2[1])/2))
	m12_11 = (int((m12_1[0] + pt1[0])/2),int((m12_1[1] + pt1[1])/2))
	m12_22 = (int((m12_2[0] + pt2[0])/2),int((m12_2[1] + pt2[1])/2))
	if(image[m12[1],m12[1]] == 0):
	   return False
	if(image[m12_1[1],m12_1[0]] == 0):
	   return False
	if(image[m12_2[1],m12_2[0]] == 0):
	   return False
	if(image[m12_22[1],m12_22[0]] == 0):
	   return False
	if(image[m12_11[1],m12_11[0]] == 0):
	   return False
	return True

def rect_contains(rect, point) :
	if point[0] < rect[0] :
		return False
	elif point[1] < rect[1] :
		return False
	elif point[0] > rect[2] :
		return False
	elif point[1] > rect[3] :
		return False
	#print point
	return True

def generate_traingle_points(r,points):

	
	subdiv  = cv2.Subdiv2D(r)
	for p in points:
		subdiv.insert(p)
	triangleList = subdiv.getTriangleList()
	return triangleList

def navMesh(world,contours, BW):

	print BW.shape
	print world.shape
	poly_contours = []
	for cnt in contours:
		epsilon = 0.0025*cv2.arcLength(cnt,True)
		contour = cv2.approxPolyDP(cnt,epsilon,True)
		poly_contours.append(contour)
	
	points = []
	for i in poly_contours:
			for coords in i:
				x,y = coords.ravel()
				points.append((x,y))
				cv2.circle(world,(x,y),1,(0,0,255),-1)

	size = world.shape[:2]
	rect = (0, 0, size[1],size[0])
	
	centroid_triangleList = generate_traingle_points(rect,points)
	path = []
	
	#Filter out points that are out of frame and are in the non-navigable areas
	for t in centroid_triangleList :
			 
		pt1 = (t[0], t[1])
		pt2 = (t[2], t[3])
		pt3 = (t[4], t[5])

		if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3) :
			centroidX = int((pt1[0] + pt2[0] + pt3[0])/3)
			centroidY = int((pt1[1] + pt2[1] + pt3[1])/3)
		
			centroid = (centroidX, centroidY)
			if(BW[centroidY, centroidX] != 0):
				cv2.circle(world,centroid,3,(255,0,0),-1)
				path.append((centroid))

	nodes_triangleList = generate_traingle_points(rect,path)
	for t in nodes_triangleList :
		pt1 = (t[0], t[1])
		pt2 = (t[2], t[3])
		pt3 = (t[4], t[5])
		if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3):
			nodes.add(pt1)
			nodes.add(pt2)
			nodes.add(pt3)

	G.add_nodes_from(nodes)

	for t in nodes_triangleList :
		pt1 = (t[0], t[1])
		pt2 = (t[2], t[3])
		pt3 = (t[4], t[5])

		
		if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3) :
			if in_navigable(BW,(pt1,pt2)):
				
				m = (int((pt1[0] + pt2[0])/2),int((pt1[1] + pt2[1])/2))
				cv2.line(world, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA, 0)
				dist = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
				G.add_edge(pt1,pt2,weight = dist)
			

			if in_navigable(BW,(pt2,pt3)):
				m = (int((pt2[0] + pt3[0])/2),int((pt2[1] + pt3[1])/2))
				cv2.line(world, pt2, pt3, (0, 255, 0), 1, cv2.LINE_AA, 0)
				dist = math.sqrt((pt2[0] - pt3[0])**2 + (pt2[1] - pt3[1])**2)
				G.add_edge(pt2,pt3, weight = dist)
				

			if in_navigable(BW,(pt3,pt1)):
				m = (int((pt3[0] + pt1[0])/2),int((pt3[1] + pt1[1])/2))
				cv2.line(world, pt3, pt1, (0, 255, 0), 1, cv2.LINE_AA, 0)
				dist = math.sqrt((pt3[0] - pt1[0])**2 + (pt3[1] - pt1[1])**2)
				G.add_edge(pt3,pt1, weight = dist)
	
	print 'Navmesh created successfully'
	cv2.imshow('World', world)
	cv2.waitKey(0)
	

