import cv2
import numpy as np
capture = cv2.VideoCapture(0)
cap_width = capture.get(3)
cap_height = capture.get(4)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while(True):
    ret,frame = capture.read()
    hsvImg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,46])
    maskBlack = cv2.inRange(hsvImg,lower_black,upper_black)
    res = cv2.bitwise_and(frame,frame,mask = maskBlack)
    resImg = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    resImg , contours, hier = cv2.findContours(resImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    
    contoursAmount = len(contours)
    rotate = 0;
    if contoursAmount>0:
        maxContours = contours[0]
        minRect = cv2.minAreaRect(maxContours) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        rotate = minRect[2]
        box = cv2.boxPoints(minRect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),1)
        x,y,w,h = cv2.boundingRect(maxContours)    
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

    text = 'rotate:%.1f'%rotate
    org = 40,80
    fontFace = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    fontColor = (0,0,255)
    thickness = 1
    lintType = 4
    bottomLeftOrigin = 1
    cv2.putText(frame,text,org,fontFace,fontScale,fontColor,thickness,lintType)
        
    cv2.imshow('frame',frame)
    cv2.waitKey(25)
