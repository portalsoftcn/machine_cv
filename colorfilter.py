import cv2
import numpy as np
import matplotlib.pyplot as plt
from util import ContourUtil, TextUtil, HSVFilteUtil
from roi import ROIDetect

contourUtil = ContourUtil()
textUtil = TextUtil()
hsvUtil = HSVFilteUtil()

lower_blue, upper_blue = hsvUtil.getFilteRange()
#lower_foot,upper_foot = hsvUtil.getFilteRange("filtefoot")
#lower_other,upper_other = hsvUtil.getFilteRange("filteother")
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

print("blue",lower_blue,upper_blue)
# blue [102 134 252] [134 255 255]
# blue [ 86  27 106] [101 255 255]
# blue [ 86  27 105] [108 255 255] iphone

# blue [ 86  27 106] [134 255 255]
# print("foot",lower_foot,upper_foot)
# print("other",lower_other,upper_other)


def showRotate(imgPath):
    frame = cv2.imread(imgPath)
    #height, width = frame.shape[:2]
    res = hsvUtil.filteByRange(frame, lower_blue, upper_blue)
    resGray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(resGray, 75, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, kernel)
    maxCnt, hierarchy = contourUtil.getMaxContour(thresh)
    contourUtil.drawRect(frame, maxCnt)
    rotate = contourUtil.drawMinRect(frame, maxCnt, hierarchy)
    rightRotate = abs(rotate)
    leftRotate = 90 - rightRotate
    text = " rotate: %.1f - %.1f" % (leftRotate ,rightRotate)
    textUtil.putText(frame, text)
    cv2.imshow(imgPath, frame)
    cv2.imwrite("case/"+imgPath, frame)

#cv2.imshow("res_blue", cv2.cvtColor(res, cv2.COLOR_BGR2HSV))

#res = hsvUtil.filteByRange(res,lower_foot,upper_foot)
#cv2.imshow("res_foot", cv2.cvtColor(res, cv2.COLOR_BGR2HSV))
#res = hsvUtil.filteByRange(res,lower_other,lower_other)
#cv2.imshow("res_other", cv2.cvtColor(res, cv2.COLOR_BGR2HSV))


#cv2.drawContours(frame, [maxCnt], 0, (0, 0, 255), 1,8,hierarchy,0,(x,y))
#rotate = contourUtil.drawMinRect(frame,maxCnt,hierarchy,offsetX,offsetY)

'''
contourUtil.drawRect(frame,maxCnt,x,y)
rotate = contourUtil.drawMinRect(frame,maxCnt,hierarchy,x,y)
thresh = cv2.erode(resGray,kernel)
thresh = cv2.dilate(thresh, es, iterations=2)
maxCnt,hierarchy = contourUtil.getMaxContour(thresh)
'''


#cv2.imshow("thresh", thresh)
'''
cv2.imshow("resGray", resGray)

'''

#showRotate("roi3.jpg")
showRotate("roi5.jpg")

cv2.waitKey()
cv2.destroyAllWindows()

'''
while True:
    ret, frame = capture.read()
    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
'''
