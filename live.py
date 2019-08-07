import os
import cv2
import subprocess as sp
import time
import requests
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
'''
serverIP9 = "192.168.1.9"
serverIP11 = "192.168.1.11"
serverIP14 = "192.168.1.14"
serverIP18 = "192.168.1.18"
uploadPath = "web/uploadimg/"
frontpath = uploadPath+"front/"
backpath = uploadPath+"back/"
leftpath = uploadPath+"left/"
rightpath = uploadPath+"right/"
toppath = uploadPath+"top/"
'''

facePath = "web/faceimg/"

faceCountArray = {"front":1,"back":1,"left":1,"right":1,"top":1}

frontCamera = cv2.VideoCapture("http://device1.portalsoft.cn:8000/?action=stream")
backCamera = cv2.VideoCapture("http://device1.portalsoft.cn:8002/?action=stream")

leftCamera = cv2.VideoCapture("http://device2.portalsoft.cn:8000/?action=stream")
rightCamera = cv2.VideoCapture("http://device2.portalsoft.cn:8002/?action=stream")

count_url = "http://localhost:8080/machine/countfileserv?"

get_now_milli_time = lambda:int( time.time() * 1000 )
slowTimes = 0

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

def getRtmpFrame(camera,lostCount):
    ###########################图片采集
    ret, currFrame = camera.read() # 逐帧采集视频流
    diff = roiDetectFront.getROIByDiff(currFrame)
    frame = processImg(currFrame,diff,lostCount)
    return frame

def getFileAmount(dir):
    files = os.listdir(dir)
    amount = len(files)
    return amount

def getAnalyseFrame(face,camera):
    '''
    read_before = get_now_milli_time()
    ret,currFrontFrame = camera.read()
    read_after = get_now_milli_time()
    '''

    analy_before = get_now_milli_time()
    analyseFrame = getRtmpFrame(camera,0)
    analy_after = get_now_milli_time()

    write_before = get_now_milli_time()
    faceAmount = faceCountArray[face]
    faceFile = facePath + face + "/"+str(faceAmount) + ".jpg"
    count_after = get_now_milli_time()
    cv2.imwrite(faceFile,analyseFrame)
    write_after = get_now_milli_time()
    #cv2.imshow(face,analyseFrame)
    faceCountArray[face] = faceAmount + 1
    requests.get(count_url,"count="+str(faceAmount))
    count_after = get_now_milli_time()
    #print("count use:"+str(count_after-write_after))
    #print("per time read use:"+str(read_after - read_before) + " analy use:" +str(analy_after - analy_before)+ " write use:"+str(write_after - write_before) + " total use:"+str(write_after - read_before))
    #print("  write detail count use:"+str(count_after - write_before)+ " write use:"+str(write_after - count_after) + " total use:"+str(write_after - write_before))
while True:
    read_before = get_now_milli_time()
    getAnalyseFrame("front",frontCamera)
    getAnalyseFrame("back",backCamera)
    getAnalyseFrame("left",leftCamera)
    #getAnalyseFrame("right",rightCamera)
    read_after = get_now_milli_time()
    fps = read_after - read_before
    if fps <= 50 :
        fps = 1000 / fps
        fps = int(fps)
        slowTimes = slowTimes + 1
        print("20 times read use:"+str(read_after - read_before)+" fps:"+str(fps) + " slow time:"+str(slowTimes))
    '''
    getAnalyseFrame("left")
    getAnalyseFrame("right")
    getAnalyseFrame("top")
    '''
    cv2.waitKey(1)
    