
#new import
import cv2
#import matplotlib.pyplot as plt
import time 
import numpy as np
from collections import deque

buffer_size = 16
points = deque(maxlen = buffer_size)

redLower = np.array([161,155,84])
redUpper = np.array([230,255,254])

prevCircle = None
dist = lambda x1,y1,x2,y2 : (x1-x2)**2 + (y1-y2)**2

video_name = "flight_test2_record.mp4"
cap = cv2.VideoCapture(video_name)

cap.set(3, 3840)
cap.set(4, 2160) 


if cap.isOpened() == False:
    print("Error")

while True:
    
    success, imgOriginal = cap.read()
    if success :
    
        #new
        ret, frame = cap.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Video", frame )
        
        grayFrame = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("deneme", grayFrame)
        
        #blur
        blurred = cv2.GaussianBlur(grayFrame, (21,21), 0)
        #cv2.imshow("deneme", blurred)

        #circle
        #param1 sensivity param2 how many edge,
        circles =cv2.HoughCircles(blurred,
                                  cv2.HOUGH_GRADIENT,
                                  1.2,
                                  100,
                                  param1    = 95,
                                  param2    = 55,
                                  minRadius = 10,
                                  maxRadius =1000)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            chosen = None
            for i in circles[0, :]:
                if chosen is None : chosen = i
                if prevCircle is not None :
                    if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(i[0],i[1],prevCircle[0],prevCircle[1]) :
                        chosen = i
            cv2.circle(imgOriginal,(chosen[0],chosen[1]),1,(0,100,100),3)
            cv2.circle(imgOriginal,(chosen[0],chosen[1]),chosen[2],(255,0,255), 3)
            prevCircle = chosen
        
        cv2.imshow("deneme", imgOriginal)
    #ret, frame = cap.read()
    #if ret == True:
    
        time.sleep(0.5) 

        cv2.imshow("Video", frame)
    
    else: break
    if cv2.waitKey(1) & 0xFF == ord("q"):break
    
cap.release()
cv2.destroyAllWindows()


#cap = cv2.cvtColor(cv2.VideoCapture(video_name), cv2.COLOR_BAYER_BG2GRAY())
#plt.figure()
#plt.imshow(cap, cmap = "gray")
#plt.axis("off")
#plt.show
#print("width: " ,cap.get(3))
#print("height: " ,cap.get(4))