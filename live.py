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

deviceIP = "192.168.1.9"
serverIP = "192.168.1.11"

def getCamera(cameraUrl):
    print(cameraUrl)
    camera = cv2.VideoCapture(cameraUrl) # 从文件读取视频
    #这里的摄像头可以在树莓派3b上使用
    if (camera.isOpened()):# 判断视频是否打开 
        print ('Open camera')
    else:
        print ('Fail to open camera!')
    return camera

def getRtmpPipe(camera,rtmpUrl):
    # 视频属性
    size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    sizeStr = str(size[0]) + 'x' + str(size[1])
    fps = camera.get(cv2.CAP_PROP_FPS)  # 30p/self
    fps = int(fps)
    hz = int(1000.0 / fps)
    print ('size:'+ sizeStr + ' fps:' + str(fps) + ' hz:' + str(hz))
    #sizeStr = '600x450'
    
    # 直播管道输出 
    # ffmpeg推送rtmp 重点 ： 通过管道 共享数据的方式
    frontCommand = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', sizeStr,
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-f', 'flv', 
        rtmpUrl]
    #管道特性配置
    pipe = sp.Popen(frontCommand, stdin=sp.PIPE) #,shell=False
    return pipe

frontCamera = getCamera("http://"+deviceIP+":8001/?action=stream")
#frontCamera = getCamera(0)
frontPipe = getRtmpPipe(frontCamera,'rtmp://'+serverIP+':1931/device/front1')

backCamera = getCamera("http://"+deviceIP+":8003/?action=stream")
#backCamera = getCamera(1)
backPipe = getRtmpPipe(backCamera,'rtmp://'+serverIP+':1931/device/back1')

leftCamera = getCamera("http://"+deviceIP+":8005/?action=stream")
#leftCamera = getCamera(2)
leftPipe = getRtmpPipe(leftCamera,'rtmp://'+serverIP+':1931/device/left1')

rightCamera = getCamera("http://"+deviceIP+":8007/?action=stream")
#rightCamera = getCamera(2)
rightPipe = getRtmpPipe(rightCamera,'rtmp://'+serverIP+':1931/device/right1')

topCamera = getCamera("http://"+deviceIP+":8009/?action=stream")
#topCamera = getCamera(2)
topPipe = getRtmpPipe(topCamera,'rtmp://'+serverIP+':1931/device/top1')

def processImg(frame,diff):
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
        
    text = " rotates: %.1f - %.1f" % (leftRotate ,rightRotate)
    textUtil.putText(frame,text)
    return frame

def getRtmpFrame(camera):
    ###########################图片采集
    ret, frame = camera.read() # 逐帧采集视频流
    diff = roiDetectFront.getROIByDiff(frame)
    frame = processImg(frame,diff)
    return frame

def pushRtmp():
    #frontFrame = getRtmpFrame(frontCamera)
    ret1,frontFrame = frontCamera.read() 
    frontPipe.stdin.write(frontFrame.tostring())  
    #cv2.imshow("frontFrame",frontFrame)
    #'''
    
    #backFrame = getRtmpFrame(backCamera)
    ret2,backFrame = backCamera.read() 
    backPipe.stdin.write(backFrame.tostring())  
    #cv2.imshow("backFrame",backFrame)
    #'''

    #leftFrame = getRtmpFrame(leftCamera)
    ret3,leftFrame = leftCamera.read() 
    leftPipe.stdin.write(leftFrame.tostring())  
    #cv2.imshow("leftFrame",leftFrame)

    #rightFrame = getRtmpFrame(rightCamera)
    ret4,rightFrame = rightCamera.read() 
    rightPipe.stdin.write(rightFrame.tostring())  
    #cv2.imshow("rightFrame",rightFrame)

    #topFrame = getRtmpFrame(topCamera)
    ret5,topFrame = topCamera.read() 
    topPipe.stdin.write(topFrame.tostring())  
    #cv2.imshow("topFrame",topFrame)

def cameraRelease():
    frontCamera.release()
    backCamera.release()
    leftCamera.release()
    rightCamera.release()
    topCamera.release()



while True:
    pushRtmp()
    key = cv2.waitKey(40)
    if key == ord('q'):
        break
cameraRelease()
