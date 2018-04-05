import serial
import time
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
#from arduino import *
from robotMQTT import *
from message import Message



robotClient = paho.Client()
robotClient.on_connect = on_connect
robotClient.on_subscribe = on_subscribe
robotClient.on_message = on_message
robotClient.on_publish = on_publish

robotClient.connect(BROKER, 1883)
robotClient.subscribe(subscribe_topic, qos = 1)


print 'loopstart'
robotClient.loop_start()


def getCPS():

	publishReq(reqID)
	if(recievedDataFlag):
		messageId = MSG.getID
		pose = MSG.getPose()
		target = MSG.getTarget
		recievedDataFlag = False

def getPose():
	return (pose[0], pose[1], pose[2])

def getNewPose():
	getCPS()
	return getPose()

def moveTo(xg,yg):

	while(True):

		(x,y,heading) = getNewPose()
		D = dist(x,y,xg,yg)
		phi = math.atan2((yg-y), (xg-x)) * 180/math.pi
		angle_error = phi - heading

		if((-5 < D < 5) and (-5 < angle_error < 5)):
			print 'Moved to ', str((x,y))
			break
		
		while(not( -5 <= angle_error <= 5)):
			rotate(angle_error)
			heading = getNewPose()[2]
			angle_error = phi - heading
		angleFlag = False

		while(not(-5 < D < 5)):

			translate(D)
			(x,y) = getNewPose()[:2]
			D = dist(x,y,xg,yg)
		distFlag = False



def rotate(angle):

	direction = 1
	if angle < 0:
		direction = 0
	ticks = int((L*10 * angle) / (math.pi * R))
	sendserData((255,255,2,ticks,direction,5,0,0))
	getserial(5)


def translate(D):

	ticks = 20 * D / (math.pi * R * PIXELTOMETER)
	sendserData((255,255,1,ticks,5,0,0,0))
	getserial(5)

