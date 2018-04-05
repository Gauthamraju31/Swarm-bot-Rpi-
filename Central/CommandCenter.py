
from ComputerVision import *
#from communications import *
import time

capture = cv2.VideoCapture(0)

while(1):
	_, frame = capture.read()

	cv2.imshow("Window", frame)
	k = cv2.waitKey(5) & 0xFF
	if k == ord('q'):
		flag = 0
		break
	if k == ord('s'):
		flag = 1
		break

if(flag):
	
	capture.set(3,FRAME_WIDTH)
	capture.set(4,FRAME_HEIGHT)

	rescuer1 = Robot(1)
	#rescuer2 = Robot(2)
	victim1 = Victim()


	calibrateField(capture)
	print 'Field Calibrated'
	#rescuer1.calibrateRobot(capture)
	#rescuer2.calibrateRobot(capture)
	#time.sleep(1)
	print 'Robots Calibrated'
	print 'Done'
	
