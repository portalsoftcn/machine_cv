import cv2
import numpy as np
from matplotlib import pyplot as plt
#
img = cv2.imread('test.jpg')
#滤波模糊
#img = cv2.blur(img,(15,15))

#过滤黑色
hsvImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_black = np.array([0,0,0])
upper_black = np.array([180,255,46])
maskBlack = cv2.inRange(hsvImg,lower_black,upper_black)
res = cv2.bitwise_and(img,img,mask = maskBlack)

'''
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(50, 50))
opened = cv2.morphologyEx(resImg, cv2.MORPH_OPEN, kernel) 
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel) 
'''

resImg = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
resImg , contours, hier = cv2.findContours(resImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 


contoursAmount = len(contours)
print("contours.length:",contoursAmount)
if contoursAmount>0:
    maxContours = contours[0]

    #epsilon = 0.01 * cv2.arcLength(maxContours,True)
    #approx = cv2.approxPolyDP(maxContours,epsilon,True)

    minRect = cv2.minAreaRect(maxContours) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    box = cv2.boxPoints(minRect)
    box = np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),1)

    x,y,w,h = cv2.boundingRect(maxContours)    
    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)



cv2.namedWindow('test',cv2.WINDOW_NORMAL)
cv2.imshow("test",img)
cv2.waitKey()
cv2.destroyAllWindows()