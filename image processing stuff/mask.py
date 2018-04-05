import numpy as np
import cv2
import time
cap = cv2.VideoCapture(1)


while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        
        height,width,depth = frame.shape

        #world=np.zeros([height,width,3],dtype=np.uint8)
        #world.fill(0)
        circle_img = np.zeros((height,width), np.uint8)
        #cv2.circle(circle_img,(width/2,height/2),280,1,thickness=-1)
        cv2.rectangle(circle_img,(height-50,50),(30,100),(100,100,0),-1)
        masked_data = cv2.bitwise_and(frame,frame, mask=circle_img)
        gray_image = cv2.cvtColor(masked_data, cv2.COLOR_BGR2GRAY)
        #ret,thresh1 = cv2.threshold(masked_data,127,255,cv2.THRESH_BINARY)
        print gray_image.shape
        cv2.imshow('masked',masked_data)
        cv2.imshow('thresh',gray_image)
        time.sleep(2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
