import os
import cv2
import subprocess as sp
import time;
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

frontCamera = cv2.VideoCapture("http://192.168.1.6:8000/?action=stream")
backCamera = cv2.VideoCapture("http://192.168.1.6:8002/?action=stream")
'''
leftCamera = cv2.VideoCapture("http://192.168.1.7:8000/?action=stream")
rightCamera = cv2.VideoCapture("http://192.168.1.7:8002/?action=stream")
'''
get_now_milli_time = lambda:int( time.time() * 1000 )

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

def getAnalyseFrame(face,camera):
    '''
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
        lostCount = 0
        analyseFrame = getRtmpFrame(currFrontFrame,lostCount)
        
        faceCountArray[face] = frameCount + 1
        faceDir = facePath + face + "/"
        faceAmount = getFileAmount(faceDir) 
        faceFile = faceDir+str(faceAmount+1) + ".jpg"
        cv2.imwrite(faceFile,analyseFrame)

    '''
    lostCount = 0
    ret,currFrontFrame = camera.read()
    analyseFrame = getRtmpFrame(currFrontFrame,lostCount)
    faceDir = facePath + face + "/"
    faceAmount = getFileAmount(faceDir) 
    faceFile = faceDir+str(faceAmount+1) + ".jpg"
    cv2.imwrite(faceFile,analyseFrame)

while True:
    read_before = get_now_milli_time()
    for i in range(1,21):
        getAnalyseFrame("front",frontCamera)
        '''
        getAnalyseFrame("back",backCamera)
        getAnalyseFrame("left",leftCamera)
        getAnalyseFrame("right",rightCamera)
        '''

    read_after = get_now_milli_time()
    print("30 times read use:"+str(read_after - read_before))
    '''
    getAnalyseFrame("back")
    getAnalyseFrame("left")
    getAnalyseFrame("right")
    getAnalyseFrame("top")
    '''