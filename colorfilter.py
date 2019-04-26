import cv2
import numpy as np
import matplotlib.pyplot as plt
from util import ContourUtil, TextUtil,HSVFilteUtil
from roi import ROIDetect

contourUtil = ContourUtil()
textUtil = TextUtil()
hsvUtil = HSVFilteUtil()

imgPath = "roi2.jpg"
frame = cv2.imread(imgPath)

hsvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_blue,upper_blue = hsvUtil.getFilteRange()
maskBlue = cv2.inRange(hsvImg, lower_blue, upper_blue)
maskBlue2=np.where((maskBlue==255),0,255).astype('uint8')

res = cv2.bitwise_and(frame, frame, mask=maskBlue2)
resGray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold( resGray , 127 , 255, cv2.THRESH_BINARY )
maxCnt = contourUtil.getMaxContour(thresh)
#contourUtil.drawRect(frame,maxCnt)
contourUtil.drawMinRect(frame,maxCnt)

cv2.imshow("resGray", resGray)
cv2.imshow("thresh", thresh)
cv2.imshow("frame", frame)
cv2.waitKey()
cv2.destroyAllWindows()

'''
while True:
    ret, frame = capture.read()
    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
'''