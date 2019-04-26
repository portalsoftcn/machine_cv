import cv2
import numpy as np
from scipy import ndimage
import sys
from util import ContourUtil,TextUtil,ImgUtil,HSVFilteUtil
from matplotlib import pyplot as plt
from roi import ROIDetect

capture = cv2.VideoCapture(0)
contourUtil = ContourUtil()
textUtil = TextUtil()
hsvUtil = HSVFilteUtil()
imgUtil = ImgUtil()
roiDetect = ROIDetect()
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
while True:
    ret, frame = capture.read()
    diff = roiDetect.getROIByDiff(frame)
    imgGray = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    imgGray = cv2.dilate(imgGray, es, iterations=2)
    maxCnt,hierarchy = contourUtil.getMaxContour(imgGray)
    rotate = 0
    if not maxCnt is None:

        x, y, w, h = cv2.boundingRect(maxCnt)
        roiImg = frame[y:y+h,x:x+w]

        imgUtil.saveImg(roiImg)

        hsvImg = cv2.cvtColor(roiImg, cv2.COLOR_BGR2HSV)
        lower_blue,upper_blue = hsvUtil.getFilteRange()
        maskBlue = cv2.inRange(hsvImg, lower_blue, upper_blue)
        maskBlue2=np.where((maskBlue==255),0,255).astype('uint8')

        res = cv2.bitwise_and(roiImg, roiImg, mask=maskBlue2)
        resGray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

        ret,thresh = cv2.threshold( resGray , 127 , 255, cv2.THRESH_BINARY )
        maxCnt,hierarchy = contourUtil.getMaxContour(thresh)

        contourUtil.drawRect(frame,maxCnt,x,y)
        rotate = contourUtil.drawMinRect(frame,maxCnt,hierarchy,x,y)
        
    text = " rotate: %.1f" % rotate
    textUtil.putText(frame,text)
    cv2.imshow("brick",frame)
    
    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
      
plt.close()
cv2.destroyAllWindows()
capture.release()
