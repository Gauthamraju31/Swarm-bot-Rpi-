import paho.mqtt.client as paho
import time
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
 
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('192.168.0.101', 1883)
client.subscribe('CPS/ROBOT/DATA', qos=1)
x="ReqPOS"
(rc, mid) = client.publish('ROBOT/DATA', x, qos=1)
client.loop_start()
#while(1):
#    (rc, mid) = client.publish('ROBOT/DATA', x, qos=1)
#    time.sleep(1)
    
