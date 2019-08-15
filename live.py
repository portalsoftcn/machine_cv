import os
import cv2
import subprocess as sp
import time
import requests
import redis
import base64
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
topCamera = cv2.VideoCapture("http://device1.portalsoft.cn:8004/?action=stream")

leftCamera = cv2.VideoCapture("http://device2.portalsoft.cn:8000/?action=stream")
rightCamera = cv2.VideoCapture("http://device2.portalsoft.cn:8002/?action=stream")

faceAmount = 1

get_now_milli_time = lambda:int( time.time() * 1000 )
slowTimes = 0

#pool = redis.ConnectionPool(host='localhost', port=6379)
#red = redis.Redis(connection_pool=pool)
red = redis.Redis(host='localhost', port=6379)

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

def storageImg(filePath,face):
    with open(filePath,"rb") as f:#转为二进制格式
        encode_before = get_now_milli_time()
        base64_data = base64.b64encode(f.read())#使用base64进行加密
        encode_after = get_now_milli_time()

        preIndex = filePath.index("/")+9
        #print(" imgKey:"+filePath[preIndex:])
        red.set(filePath[preIndex:],base64_data)
        storage_after = get_now_milli_time() 
        os.remove(filePath)
        print("storage encode use:"+str(encode_after - encode_before) + " db use:"+str(storage_after - encode_after) + " len:"+str(len(base64_data)))
    
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
    
    faceFile = facePath + face + "/"+str(faceAmount) + ".jpg"
    #print("faceFile:"+faceFile)
    writeImg = cv2.resize(analyseFrame,(400,300),interpolation=cv2.INTER_CUBIC) 
    cv2.imwrite(faceFile,writeImg)
    write_after = get_now_milli_time()
    storageImg(faceFile,face)
    storage_after = get_now_milli_time()
    #cv2.imshow(face,writeImg)
    #print("count use:"+str(count_after-write_after))
    #if (read_after - read_before) >= 10 :
    print(face+" face  analy use:" +str(analy_after - analy_before)+ " write use:"+str(write_after - write_before) + " total use:"+str(storage_after - analy_before))
    #print("  write detail  save use:"+str(write_after - write_before) + " db use: "+str(storage_after - write_after)+" total use:"+str(storage_after - write_before))

while True:
    read_before = get_now_milli_time()

    getAnalyseFrame("front",frontCamera)
    getAnalyseFrame("back",backCamera)
    getAnalyseFrame("top",topCamera)
    getAnalyseFrame("left",leftCamera)
    getAnalyseFrame("right",rightCamera)
    red.set("count",faceAmount)

    read_after = get_now_milli_time()
    fps = read_after - read_before
    fps = 1000 / fps
    fps = int(fps)
    if fps <25 :
        slowTimes = slowTimes + 1
    print("*****************************************process use:"+str(read_after - read_before)+" fps:"+str(fps) + " slow time:"+str(slowTimes))
    faceAmount = faceAmount + 1
    