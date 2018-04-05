import serial
import time
import paho.mqtt.client as paho
import paho.mqtt.publish as publish


BROKER = '192.168.0.101'
port = '//dev//USB0'
arduino = serial.Serial(port, 9600)
subscribe_topic = 'Central/Data'
messageRecvd  =False
dataId = 0

def sendserData(serialData):
	for x in serialData:
		arduino.write(chr(x))

def decodeData(data):

	decodedData = []
	l = []
	a = data.split('/')
	for x in a:
		l.append(eval(x))
	decodedData.append(l)

	print decodedData

def on_message(client, userdata, msg):
	print msg.topic + str(msg.payload)
	decodeData(msg.payload)
	global messageRecvd
	messageRecvd = True
	
def on_subscribe(client, userdata, mid, granted_qos):
	print 'Subscribed: ' + str(mid)

client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(BROKER, 1883)
client.subscribe(subscribe_topic, qos = 1)

print 'loopstart'
client.loop_forever()



def moveTo(target, theta):

	getPose()
	position = decodeData[1]
	distance = math.sqrt((position[0] - target[0])**2 + (position[1] - target[1])**2)
	omega = math.atan2((target[1] - position[1])/(target[0] - position[0]))*180/math.pi
	theta = position[2]
	delta = omega + theta
	error = omega - theta
	permitable = 5
	while(error > permitable and error < (-1* permitable)):
		if(omega > 0):
			sendserData((255,255,6,delta,1))
			time.sleep(1)
		if(omega < 0):
			sendserData((255,255,6,delta,0))
			time.sleep(1)

		getPose()
		theta = decodeData[dataId][1][2]
		error = omega - theta
		delta = omega + theta

	real_dist = distance / pixel_meter_factor
	sendserData((255,255,1,real_dist)
	


