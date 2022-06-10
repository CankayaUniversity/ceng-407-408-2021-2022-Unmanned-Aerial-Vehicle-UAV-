import cv2
import numpy as np
from collections import deque

#nesne merkezini depolayacak veri tipi
buffer_size = 16
points = deque(maxlen = buffer_size)

#kırmızı renk aralıgı
redLower = np.array([161,155,84])
redUpper = np.array([230,255,254])

prevCircle = None
dist = lambda x1,y1,x2,y2 : (x1-x2)**2 + (y1-y2)**2

#capture
cap = cv2.VideoCapture(1)

#new part
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(width, height)

#new video kaydet
writer = cv2.VideoWriter("flight_test2_record.mp4", cv2.VideoWriter_fourcc(*"DIVX"),20,(width, height))

#cap.set(3, 960)
#cap.set(4, 480) 

while True :
    
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
        #hsv
        #hsv = cv2.cvtColor(blurred , cv2.COLOR_BGR2HSV)
        #cv2.imshow("deneme", hsv)
        
        #mask = cv2.inRange(hsv,redLower,redUpper)
        #cv2.imshow("deneme", mask)
          
    
    #new save
    writer.write(frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):break

cap.release()
writer.release()
cv2.destroyAllWindows()        
  
    
#cv2.destroyAllWindows()

#cap.release() 