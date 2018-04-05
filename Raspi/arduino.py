#ARDUINO INTERFACE
import serial
import time

port = '/dev/ttyUSB0'
arduino = serial.Serial(port, 9600)
time.sleep(2)

def sendserData(serialData):
	for x in serialData:
		arduino.write(chr(x))

def getserial(packetlength):
    #print "Serial in waiting ", ser.inWaiting()
    if ser.inWaiting()>=packetlength:
        preamble1 = ord(ser.read())
        if preamble1 == 255:
            if ord(ser.read()) == 255:
 
                x = ser.read(packetlength-2) 
                a = [ord(x) for x in x]

                if ser.inWaiting()>0:            #if any data is left in input buffer following the read of a packet
                    ser.read(ser.inWaiting())    #read what is left to clear data from buffer.
                                                 #This ensures next data packet read is the most up to date data
                return a
