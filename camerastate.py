import cv2
import numpy as np

class CameraState:

    frontFace = "front"
    rightFace = "right"
    topFace = "top"

    cameraIndex = 0

    def __init__(self,faceType):
        if faceType == self.frontFace :
            index = 0
        elif faceType == self.rightFace :
            index = 1
        elif faceType == self.topFace :
            index = 2
        self.cameraIndex = index

    def getFaceState(self):
        rotate = 0
        capture = cv2.VideoCapture(self.cameraIndex)
        ret,frame = capture.read()
        hsvImg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_black = np.array([0,0,0])
        upper_black = np.array([180,255,46])
        maskBlack = cv2.inRange(hsvImg,lower_black,upper_black)
        res = cv2.bitwise_and(frame,frame,mask = maskBlack)
        resImg = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        resImg , contours, hier = cv2.findContours(resImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
        contoursAmount = len(contours)
        if contoursAmount>0:
            maxContours = contours[0]
            minRect = cv2.minAreaRect(maxContours) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            rotate = minRect[2]
            box = cv2.boxPoints(minRect)
            box = np.int0(box)
            cv2.drawContours(frame,[box],0,(0,0,255),1)
            x,y,w,h = cv2.boundingRect(maxContours)    
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        return rotate,frame
