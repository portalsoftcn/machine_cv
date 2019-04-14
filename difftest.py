import cv2
import numpy as np
from scipy import ndimage
from util import ContourUtil,TextUtil

capture = cv2.VideoCapture(0)
contourUtil = ContourUtil()
textUtil = TextUtil()
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
background = None
rotate = 0

while True:

    ret, frame = capture.read()
    
    '''
    frameGray = cv2.cvtColor( frame.copy() , cv2.COLOR_BGR2GRAY )
    ret , thresh = cv2.threshold( frameGray ,130,255,cv2.THRESH_BINARY )
    cnts = contourUtil.getContours(thresh)
    contourUtil.drawContours(frame,cnts)
    '''
    
    if background is None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (5, 5), 0)
        continue
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    diff = cv2.absdiff(background, gray_frame)
    diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)

    maxCnt = contourUtil.getMaxContour(diff.copy())
    contourUtil.drawRect(frame,maxCnt)
    brickImg = frame
    if not maxCnt is None:
        x, y, w, h = cv2.boundingRect(maxCnt)
        

    '''
    rotate = contourUtil.drawMinRect(frame, maxCnt)
    text = " rotate: %.1f" % rotate
    textUtil.putText(frame,text)
    '''
    cv2.imshow("brickImage", brickImg)

    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
capture.release()
