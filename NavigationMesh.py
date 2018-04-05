import cv2
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy import spatial
import time


G = nx.Graph()
font = cv2.FONT_HERSHEY_SIMPLEX

def distance(pt1, pt2):
	return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def nearest(points, k, point):
	dist = []
	D = {}
	neighbours = []
	for pt in points:
		#print pt
		#print point
		d = distance(point, pt)
		dist.append(d)
		D[d] = pt
	dist.sort()
	dist = dist[:k]
	for d in dist:
		neighbours.append(D[d])
	return neighbours

def localPlanner(image, pt1, pt2):
	
	theta = math.atan2((pt2[1] - pt1[1]), (pt2[0] - pt1[0]))
	r = 2
	flag = True
	x = pt1[0]
	y = pt1[1]
	
	while r <= distance(pt1, pt2):
		#print 'Here'
		xPrime = int(x + r * math.cos(theta))
		yPrime = int(y + r * math.sin(theta))
		qPrime = (xPrime,yPrime)
		robotDiag = 20
		corner1 = qPrime + robotDiag * np.array([math.sin(theta - math.pi/4) , math.cos(theta - math.pi/4)])
		corner2 = qPrime + robotDiag * np.array([math.sin(theta + math.pi/4) , math.cos(theta + math.pi/4)])
		corner3 = qPrime + robotDiag * np.array([math.sin(theta + math.pi -  math.pi/4) , math.cos(theta + math.pi - math.pi/4)])
		corner4 = qPrime + robotDiag * np.array([math.sin(theta + math.pi + math.pi/4) , math.cos(theta + math.pi +  math.pi/4)])
		
		corner1 = corner1.astype(int)
		corner2 = corner2.astype(int)
		corner3 = corner3.astype(int)
		corner4 = corner4.astype(int)


		if(collisionFree(image, qPrime) and collisionFree(image, corner1) and collisionFree(image, corner2) and collisionFree(image, corner3) and collisionFree(image, corner4)):
			#print 'Here'
			#cv2.circle(image, qPrime, 2, (255,0,0), -1)
			r = r + 1
		else:
			flag = False
			break
		
	return flag

def PRM(image, n,k):
	dmin = 40
	V = set()
	E = set()
	#print image.shape[:2]
	i = 0
	while i < n:
		sample = ()
		randomList = [random.random(), random.random()]
		R = np.array(randomList).reshape(1,2)
		q = (R * image.shape[:2])[0]
		q = q[::-1]
		q = tuple(map(int, q))



		#print q
		#cv2.circle(image, q, 5, (255,0,0), -1)
		if(collisionFree(image,q) and (20 < q[0] < image.shape[1] - 20) and (20 < q[1] < image.shape[0] - 20)):
			V.add(q)
			i = i + 1
			#cv2.circle(image, q, 3, (0,0,255), -1)

	V = list(V)
	#print V
	for i in range(len(V)):
		q = V[i]
		neighbours = nearest(V[i+1:], k, q)
		for qPrime in neighbours:
			edge = (q, qPrime)
			if localPlanner(image,q,qPrime):
				#print 'Adding edge'
				E.add(edge)
	#print E
	for e in E:
		#print e
		pt1 = e[0]
		pt2 = e[1] 
		#cv2.line(image, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA, 0)

	return set(V), E

def addEdge(pt1, pt2):
	
	G.add_edge(pt1, pt2, weight = distance(pt1, pt2))

def collisionFree(image,point):


	imgWidth = image.shape[0]
	imgHeight = image.shape[1]
	#print imgWidth
	#print imgHeight

	if ((0 < point[1] < imgWidth) and (0 < point[0] < imgHeight)):
		try:
			value = image[point[1], point[0],0]
		except IndexError:
			print (point)
		#print 'Point', point
		#print 'Value', value
		if(value == 0):
			#cv2.circle(image, point , 2, (0,0,255), -1)
			#print 'Inside'
			return False
		else:
			#cv2.circle(image, point , 2, (255,0,0), -1)
			#print 'outside'
			return True
	else:
		return False

img = cv2.imread("D:\\SWARM ROBOTICS\\IMAGE PROCESSING\\SampleWorld.jpg",1)
imgCpy = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (5,5), 3)
imgThreshold = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)[1]


imgErode = cv2.erode(imgThreshold, (3,3), iterations = 1)
imgDilate = cv2.dilate(imgErode, (3,3), iterations = 1)

for i in range(10):
	imgErode = cv2.erode(imgDilate, (5,5), iterations = 1)
	imgDilate = cv2.dilate(imgErode, (9,9), iterations = 1)

_,contours,_ = cv2.findContours(imgDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

filteredContours = []

factor = 0.002
for contour in contours:
	area = cv2.contourArea(contour)
	#print len(contour)
	epsilon = factor * cv2.arcLength(contour,True)
	approxContour = cv2.approxPolyDP(contour, epsilon, False)
	#print len(approxContour)
	filteredContours.append(approxContour)


output = np.zeros([imgThreshold.shape[0], imgThreshold.shape[1],3], np.uint8)
output.fill(255)

cv2.drawContours(output , filteredContours , -1 , 0, cv2.FILLED)
output = cv2.bitwise_not(output)



t1 = time.time()
#localPlanner(output, (27,8), (66,192))
V,E = PRM(output,250,5)

#for vertex in V:
#	cv2.circle(output, vertex , 2, (255,0,0), -1)
	
#for edge in E:
#	cv2.line(output, edge[0], edge[1], (0, 255, 0), 1, cv2.LINE_AA, 0)

G.add_nodes_from(V)

for edge in E:
	addEdge(edge[0], edge[1])

cv2.circle(output, (20,20) , 2, (0,0,255), -1)
cv2.circle(output, (80,20) , 2, (0,0,255), -1)


start = V.pop()
#cv2.circle(output, start , 2, (255,0,0), -1)
end = V.pop()
#cv2.circle(output, end , 2, (0,0,255), -1)

path = None
if(nx.has_path(G, start, end)):
	path = nx.dijkstra_path(G, start, end)


if path != None:
	for i in range(len(path) - 1):
	    pt1 = path[i]
	    pt2 = path[i+1]
	    #cv2.line(output, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA, 0)
t2 = time.time()
print (t2-t1)

cv2.imshow("Input", img)
cv2.imshow("Output", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
