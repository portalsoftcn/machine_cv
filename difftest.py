import cv2
import numpy as np
from scipy import ndimage
import sys
from util import ContourUtil,TextUtil,ImgUtil,HSVFilteUtil
from matplotlib import pyplot as plt
from roi import ROIDetect

capture = cv2.VideoCapture("http://192.168.1.8:8002/?action=stream")
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280) 
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720) 
contourUtil = ContourUtil()
textUtil = TextUtil()
hsvUtil = HSVFilteUtil()
imgUtil = ImgUtil()
roiDetect = ROIDetect()
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2))

lower_blue,upper_blue = hsvUtil.getFilteRange()
#print("blue_range",lower_blue,upper_blue)
#lower_foot,upper_foot = hsvUtil.getFilteRange("filtefoot")
#lower_other,upper_other = hsvUtil.getFilteRange("filteother")
#lower_finger,upper_finger = hsvUtil.getFilteRange("filtefinger")

maxRotate = 0
while True:
    ret, frame = capture.read()
    
    diff = roiDetect.getROIByDiff(frame)
    imgGray = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    imgGray = cv2.dilate(imgGray, es, iterations=2)
    maxCnt,hierarchy = contourUtil.getMaxContour(imgGray)
    leftRotate = 0
    rightRotate = 0
    if not maxCnt is None:

        x, y, w, h = cv2.boundingRect(maxCnt)
        roiImg = frame[y:y+h,x:x+w]

        #imgUtil.saveImg(roiImg)

        res = hsvUtil.filteByRange(roiImg,lower_blue,upper_blue)

        resGray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold( resGray , 75 , 255, cv2.THRESH_BINARY )
        thresh = cv2.erode(thresh,kernel)
        maxCnt,hierarchy = contourUtil.getMaxContour(thresh)

        #cv2.drawContours(frame, [maxCnt], 0, (0, 0, 255), 1,8,hierarchy,0,(x,y))

        contourUtil.drawRect(frame,maxCnt,x,y)
        rotate = contourUtil.drawMinRect(frame,maxCnt,hierarchy,x,y)
        rightRotate = abs(rotate)
        leftRotate = 90 - rightRotate
        '''
        maxLR = max(leftRotate,rightRotate)
        maxRotate = max(maxLR,maxRotate)
        if maxRotate >= maxLR:
            maxRotate = maxLR
        '''
        #cv2.imshow("frame",frame)
        #cv2.imshow("res",res)
        #cv2.imshow("thresh",thresh)
        
    text = " rotates: %.1f - %.1f" % (leftRotate ,rightRotate)
    textUtil.putText(frame,text)
    cv2.imshow("brick",frame)
    key = cv2.waitKey(1000//40)
    if key == ord('q'):
        break
    elif key == ord('a'):
        print('a')
    elif key == ord('s'):
        print('')
    
plt.close()
cv2.destroyAllWindows()
capture.release()
