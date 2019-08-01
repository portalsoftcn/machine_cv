import os
import cv2
import subprocess as sp
from util import ContourUtil,TextUtil,ImgUtil,HSVFilteUtil
from roi import ROIDetect

roiDetectFront = ROIDetect()
contourUtil = ContourUtil()
textUtil = TextUtil()
hsvUtil = HSVFilteUtil()
imgUtil = ImgUtil()

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2))

lower_blue,upper_blue = hsvUtil.getFilteRange()

#业务数据计算

serverIP9 = "192.168.1.9"
serverIP11 = "192.168.1.11"
serverIP14 = "192.168.1.14"
serverIP18 = "192.168.1.18"

uploadPath = "web/uploadimg/"
facePath = "web/faceimg/"
frontpath = uploadPath+"front/"
backpath = uploadPath+"back/"
leftpath = uploadPath+"left/"
rightpath = uploadPath+"right/"
toppath = uploadPath+"top/"

faceCountArray = {"front":0,"back":0,"left":0,"right":0,"top":0}

def processImg(frame,diff,lostCount):
    imgGray = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    imgGray = cv2.dilate(imgGray, es, iterations=2)
    maxCnt,hierarchy = contourUtil.getMaxContour(imgGray)
    leftRotate = 0
    rightRotate = 0
    if not maxCnt is None:

        x, y, w, h = cv2.boundingRect(maxCnt)
        roiImg = frame[y:y+h,x:x+w]
        res = hsvUtil.filteByRange(roiImg,lower_blue,upper_blue)

        resGray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold( resGray , 75 , 255, cv2.THRESH_BINARY )
        thresh = cv2.erode(thresh,kernel)
        maxCnt,hierarchy = contourUtil.getMaxContour(thresh)

        contourUtil.drawRect(frame,maxCnt,x,y)
        rotate = contourUtil.drawMinRect(frame,maxCnt,hierarchy,x,y)
        rightRotate = abs(rotate)
        leftRotate = 90 - rightRotate
        
    text = " rotates: %.1f - %.1f  lost:%d" % (leftRotate ,rightRotate,lostCount)
    textUtil.putText(frame,text)
    return frame

def getRtmpFrame(currFrame,lostCount):
    ###########################图片采集
    #ret, frame = camera.read() # 逐帧采集视频流
    diff = roiDetectFront.getROIByDiff(currFrame)
    frame = processImg(currFrame,diff,lostCount)
    return frame

def getFileAmount(dir):
    files = os.listdir(dir)
    amount = len(files)
    return amount

def getAnalyseFrame(face):
    uploadDir = uploadPath + face + "/"
    amount = getFileAmount(uploadDir)
    frameCount = faceCountArray[face]

    if frameCount < amount:
        if frameCount <= 1:
            frameCount = 1
        else:
            frameCount = amount - 1  
        
        lostCount = frameCount -  faceCountArray[face] 
        currFrontFrame = cv2.imread(uploadDir+str(frameCount)+".jpg")
        analyseFrame = getRtmpFrame(currFrontFrame,lostCount)
        
        faceCountArray[face] = frameCount + 1
        faceDir = facePath + face + "/"
        faceAmount = getFileAmount(faceDir) 
        faceFile = faceDir+str(faceAmount+1) + ".jpg"
        cv2.imwrite(faceFile,analyseFrame)

while True:
    getAnalyseFrame("front")
    getAnalyseFrame("back")
    getAnalyseFrame("left")
    getAnalyseFrame("right")
    getAnalyseFrame("top")
