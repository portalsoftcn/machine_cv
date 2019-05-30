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

def getCamera(cameraUrl):
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
    #sizeStr = '400x300'
    fps = camera.get(cv2.CAP_PROP_FPS)  # 30p/self
    fps = int(fps)
    hz = int(1000.0 / fps)
    print ('size:'+ sizeStr + ' fps:' + str(fps) + ' hz:' + str(hz))
    #fps = 12

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

def getRtmpFrame(camera):
    ###########################图片采集
    ret, frame = camera.read() # 逐帧采集视频流
    diff = roiDetectFront.getROIByDiff(frame)
    frame = processImg(frame,diff)
    return frame

def pushRtmp():
    frontFrame = getRtmpFrame(frontCamera)
    frontPipe.stdin.write(frontFrame.tostring())  
    '''
    #frontFrame = getRtmpFrame(frontCamera)
    backPipe.stdin.write(frontFrame.tostring())  

    leftFrame = getRtmpFrame(leftCamera)
    leftPipe.stdin.write(leftFrame.tostring())  

    #leftFrame = getRtmpFrame(leftCamera)
    topPipe.stdin.write(leftFrame.tostring())  

    #leftFrame = getRtmpFrame(leftCamera)
    rightPipe.stdin.write(leftFrame.tostring())  
    '''

#业务数据计算
frontCamera = None
leftCamera = None
topCamera = None
rightCamera = None
backCamera = None

frontCamera = getCamera("http://192.168.1.12:8001/?action=stream")
frontPipe = getRtmpPipe(frontCamera,'rtmp://127.0.0.1:1931/front/mystream')

backPipe = getRtmpPipe(frontCamera,'rtmp://127.0.0.1:1931/back/mystream')

leftCamera = getCamera("http://192.168.1.12:8003/?action=stream")
leftPipe = getRtmpPipe(frontCamera,'rtmp://127.0.0.1:1931/left/mystream')

topPipe = getRtmpPipe(leftCamera,'rtmp://127.0.0.1:1931/top/mystream')

rightPipe = getRtmpPipe(leftCamera,'rtmp://127.0.0.1:1931/right/mystream')

def cameraRelease():
    frontCamera.release()
    leftCamera.release()
    #topCamera.release()
    #rightCamera.release()
    #backCamera.release()

while True:
    pushRtmp()
cameraRelease()
