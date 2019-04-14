import cv2
import numpy as np

class ContourUtil:
    def __init__(self):pass

    def getMaxContour(self,srcImg):
        maxCnt = None
        cnts, hierarchy = cv2.findContours(
        srcImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in cnts:
            if (maxCnt is None) or cv2.contourArea(cnt) >= cv2.contourArea(maxCnt):
                maxCnt = cnt
        return maxCnt
    
    def drawRect(self,srcImg,cnt):
        if not cnt is None:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(srcImg, (x, y), (x+w, y+h), (0, 255, 0), 1)
    
    def drawMinRect(self,srcImg,cnt):
        rotate = 0
        if not cnt is None:
            minRect = cv2.minAreaRect(cnt)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            rotate = minRect[2]
            box = cv2.boxPoints(minRect)
            box = np.int0(box)
            cv2.drawContours(srcImg, [box], 0, (0, 0, 255), 1)
        return rotate

class TextUtil:
    def __init__(self):pass
    
    def putText(self,srcImg,text):
        org = 40, 80
        fontFace = cv2.FONT_HERSHEY_COMPLEX
        fontScale = 1
        fontColor = (0, 0, 255)
        thickness = 1
        lintType = 4
        cv2.putText(srcImg, text, org, fontFace, fontScale,
                fontColor, thickness, lintType)