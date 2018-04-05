from message import Message
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
from settings import *
	

def on_message(client, userdata, msg):
	
	global recievedDataFlag
	global MSG
	global msgid
	print msg.topic + str(msg.payload)
	recievedDataFlag = True
	MSG = Message(msgid,msg.payload)
	MSG.splitPayload()
	print MSG.getPose()
	
	msgid += 1
	
	
def on_subscribe(client, userdata, mid, granted_qos):
	print 'Subscribed: ' + str(mid)

def on_publish(client, userdata, mid):

	print ('mid: ' + str(mid))

def on_connect(client, userdata, rc):
	client.subscribe(subscribe_topic, 0)
	print ('rc: ' + str(rc))

def publishReq(number):
	
	global reqid
	msg = 'ReqPOS'+ str(reqid)
	client.publish(publish_topic,msg, qos = 1)
	reqid += 1

