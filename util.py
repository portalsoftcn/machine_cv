import cv2
import numpy as np
import time
import os

class ContourUtil:
    def __init__(self):pass

    def getContours(self,srcImg):
        cnts, hierarchy = cv2.findContours(
        srcImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cnts,hierarchy
    
    def drawContours(self,srcImg,cnts):
        cv2.drawContours(srcImg,cnts,-1,(0,0,255),1)

    def getMaxContour(self,srcImg):
        maxCnt = None
        cnts , hierarchy = self.getContours(srcImg)
        for cnt in cnts:
            if (maxCnt is None) or cv2.contourArea(cnt) >= cv2.contourArea(maxCnt):
                maxCnt = cnt
        return maxCnt,hierarchy
    
    def drawRect(self,srcImg,cnt,offsetX=0,offsetY=0):
        if not cnt is None:
            x, y, w, h = cv2.boundingRect(cnt)
            x = offsetX + x
            y = offsetY + y
            cv2.rectangle(srcImg, (x, y), (x+w, y+h), (0, 255, 0), 1)
    
    def drawMinRect(self,srcImg,cnt,hierarchy,offsetX=0,offsetY=0):
        rotate = 0
        if not cnt is None:
            minRect = cv2.minAreaRect(cnt)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            rotate = minRect[2]
            box = cv2.boxPoints(minRect)
            box = np.int0(box)
            cv2.drawContours(srcImg, [box], 0, (0, 0, 255), 1,8,hierarchy,0,(offsetX,offsetY))
        return rotate

class TextUtil:
    def __init__(self):pass
    
    def putText(self,srcImg,text):
        org = 40, 80
        fontFace = cv2.FONT_HERSHEY_COMPLEX
        fontScale = 1
        fontColor = (0, 0, 0)
        thickness = 1
        lintType = 4
        cv2.putText(srcImg, text, org, fontFace, fontScale,
                fontColor, thickness, lintType)

class ImgUtil:
    def __init__(self):pass
    
    def sobelImg(self,srcImg):
        x=cv2.Sobel(srcImg,cv2.CV_16S,1,0)
        y=cv2.Sobel(srcImg,cv2.CV_16S,0,1)

        absx=cv2.convertScaleAbs(x)
        absy=cv2.convertScaleAbs(y)
        dist=cv2.addWeighted(absx,1.5,absy,1.5,0)

        return dist

    def saveImg(self,srcImg):
        date = time.strftime("%Y%m%d%H%M", time.localtime()) 
        cv2.imwrite("test/%s.jpg"%date,srcImg)

class HSVFilteUtil:
    def __init__(self): pass

    def getFilteRange(self,dir='filtebg/'):
        
        minH = 255
        minS = 255
        minV = 255
        maxH = 0
        maxS = 0
        maxV = 0

        path = os.getcwd()+"/"+dir+"/"
        filelist = os.listdir(path)
        for p in filelist:
            if ".jpg" in p :
                imgPath = path+p
                frame = cv2.imread(imgPath)
                hsvImg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h,w = hsvImg.shape[:2]
                for row in range(1, h):
                    for col in range(1, w):
                        pixItem = hsvImg[row][col]
                        pixH = pixItem[0]
                        pixS = pixItem[1]
                        pixV = pixItem[2]
                        minH = min(pixH, minH)
                        minS = min(pixS, minS)
                        minV = min(pixV, minV)
                        maxH = max(pixH, maxH)
                        maxS = max(pixS, maxS)
                        maxV = max(pixV, maxV)

        lower_range = np.array([minH, minS, minV])
        upper_range = np.array([maxH, maxS, maxV])
        #print("imgIndex--:",(minH, minS, minV),(maxH, maxS, maxV))
        return lower_range,upper_range