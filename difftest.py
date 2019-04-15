import cv2
import numpy as np
from scipy import ndimage
from util import ContourUtil,TextUtil
from matplotlib import pyplot as plt
from roi import ROIDetect

capture = cv2.VideoCapture(0)
contourUtil = ContourUtil()
textUtil = TextUtil()
roiDetect = ROIDetect()
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
background = None
rotate = 0

while True:

    ret, frame = capture.read()
    
    if background is None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (11, 11), 0)
        continue
    
    maxCnt = roiDetect.getROIContour(background,frame)
    
    contourUtil.drawRect(frame,maxCnt)
    brickImg = frame

    '''
    rotate = contourUtil.drawMinRect(frame, maxCnt)
    text = " rotate: %.1f" % rotate
    textUtil.putText(frame,text)
    '''
    '''
    plt.close()

    plt.subplot(121),plt.imshow( cv2.cvtColor(brickImg,cv2.COLOR_BGR2RGB)  )
    plt.title("brick"),plt.xticks([]),plt.yticks([])

    plt.subplot(122),plt.imshow(cv2.cvtColor(diff,cv2.COLOR_BGR2RGB))
    plt.title("diff"),plt.xticks([]),plt.yticks([])
    
    plt.show() 
    '''
    cv2.imshow("brick",frame)
    
    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
      
plt.close()
cv2.destroyAllWindows()
capture.release()
