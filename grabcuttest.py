import cv2
import numpy as np
import matplotlib.pyplot as plt
from util import ContourUtil,TextUtil
from roi import ROIDetect

imgPath = "roi4.jpg"

contourUtil = ContourUtil()

img = cv2.imread(imgPath)

'''
offset = 2
imgSize = img.shape[:2]
imgW = imgSize[0]
imgH = imgSize[1]
roiImg = img[offset:imgW-offset,offset:imgH-offset]
cv2.imwrite(imgPath,roiImg)
'''
'''
x=cv2.Sobel(img,cv2.CV_16S,1,0)
y=cv2.Sobel(img,cv2.CV_16S,0,1)

absx=cv2.convertScaleAbs(x)
absy=cv2.convertScaleAbs(y)
dist=cv2.addWeighted(absx,1.5,absy,1.5,0)


ret,thresh = cv2.threshold(imgGray,150,255,0)

maxCnt = contourUtil.getMaxContour(thresh)
contourUtil.drawRect(img,maxCnt)

#cnts,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(img,cnts,-1,(0,0,255),1)
'''
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel = np.ones((9,9),np.uint8)
closing = cv2.morphologyEx(imgGray, cv2.MORPH_CLOSE, kernel)

cv2.imshow("gray",imgGray)
cv2.imshow("closing",closing)
cv2.waitKey()
cv2.destroyAllWindows()


'''
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
imgGray = cv2.threshold(imgGray, 30, 255, cv2.THRESH_BINARY)[1]
imgGray = cv2.dilate(imgGray, es, iterations=2)
imgGray = cv2.GaussianBlur(imgGray, (15, 15), 0)
cnts,hierarchy = cv2.findContours(imgGray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(img,cnts,-1,(0,0,255),1)
cv2.imshow('dsit',dist)
cv2.imshow('gray',imgGray)
cv2.waitKey(0)
cv2.destroyAllWindows()

img=cv2.imread("roi1.jpg")
size = img.shape[:2]
mask=np.zeros((img.shape[:2]),np.uint8)
bgdModel=np.zeros((1,65),np.float64)
fgdModel=np.zeros((1,65),np.float64)
rect=(50,25,size[0]-20,size[1])
rect=(50,0,size[0],size[1])
#这里计算了5次
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,2,cv2.GC_INIT_WITH_RECT)
#关于where函数第一个参数是条件，满足条件的话赋值为0，否则是1。如果只有第一个参数的话返回满足条件元素的坐标。
mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
#mask2就是这样固定的

imgTarget=img*mask2[:,:,np.newaxis]

imgGray = cv2.cvtColor(imgTarget,cv2.COLOR_BGR2GRAY)

contourUtil = ContourUtil()

maxCnt = contourUtil.getMaxContour(imgGray)
    
contourUtil.drawMinRect(img,maxCnt)

plt.subplot(1,2,1)
plt.imshow( cv2.cvtColor(img,cv2.COLOR_BGR2RGB) )
plt.title('original image ')
plt.xticks([])
plt.yticks([])
plt.subplot(1,2,2)
#这里的img也是固定的。

plt.imshow( cv2.cvtColor(imgTarget,cv2.COLOR_BGR2RGB) )
plt.title('target image')
plt.xticks([])
plt.yticks([])
plt.show()

img = cv2.imread('roi1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''