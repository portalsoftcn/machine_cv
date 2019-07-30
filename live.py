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

#deviceIP = "192.168.1.9"

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

faceCountArray = {"front":1,"back":1,"left":1,"right":1,"top":1}

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
    #ffmpeg -hwaccel cuvid -c:v h264_cuvid -i rtmp://192.168.1.14:1931/yun/right -vcodec h264_nvenc -f flv  rtmp://192.168.1.14:1931/device/right

    frontCommand = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', sizeStr,
        '-r', str(fps),
        '-i', '-',
        '-vcodec', 'h264_nvenc',
        '-f', 'flv', 
        rtmpUrl]

    #管道特性配置
    pipe = sp.Popen(frontCommand, stdin=sp.PIPE) #,shell=False
    return pipe
'''
frontCamera = getCamera('rtmp://'+serverIP14+':1931/yun/front')
frontPipe = getRtmpPipe(frontCamera,'rtmp://'+serverIP14+':1931/device/front')

backCamera = getCamera('rtmp://'+serverIP14+':1931/yun/back')
backPipe = getRtmpPipe(backCamera,'rtmp://'+serverIP14+':1931/device/back')

leftCamera = getCamera('rtmp://'+serverIP14+':1931/yun/left')
leftPipe = getRtmpPipe(leftCamera,'rtmp://'+serverIP14+':1931/device/left')

rightCamera = getCamera("http://192.168.1.18:8003/?action=stream")
rightPipe = getRtmpPipe(rightCamera,'rtmp://'+serverIP14+':1931/device/right')

topCamera = getCamera("http://"+deviceIP+":8009/?action=stream")
topPipe = getRtmpPipe(topCamera,'rtmp://'+serverIP+':1931/device/top1')
'''

'''
frontCamera = getCamera("http://"+serverIP18+":8001/?action=stream")
backCamera = getCamera("http://"+serverIP18+":8003/?action=stream")
leftCamera = getCamera("http://"+serverIP14+":8003/?action=stream")
rightCamera = getCamera("http://"+serverIP14+":8003/?action=stream")
topCamera = getCamera("http://"+serverIP14+":8003/?action=stream")
'''


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

def getRtmpFrame(currFrame):
    ###########################图片采集
    #ret, frame = camera.read() # 逐帧采集视频流
    diff = roiDetectFront.getROIByDiff(currFrame)
    frame = processImg(currFrame,diff)
    return frame

def getFileAmount(dir):
    files = os.listdir(dir)
    amount = len(files)
    return amount

def removeFile(dir):
    amount = getFileAmount(dir)
    if amount > 1:
        #delete 1.jpg
        #rename 2.jpg to 1.jpg
        os.remove(dir+"1.jpg")
        os.rename(dir+"2.jpg",dir+"1.jpg")

def getAnalyseFrame(face):
    uploadDir = uploadPath + face + "/"
    amount = getFileAmount(uploadDir)
    frameCount = faceCountArray[face]
    '''
    if frameCount < amount:
        if frameCount <= 1:
            frameCount = 1
        else:
            frameCount = amount - 1  
        currFrontFrame = cv2.imread(uploadDir+str(frameCount)+".jpg")
        analyseFrame = getRtmpFrame(currFrontFrame)
        
        faceCountArray[face] = frameCount + 1
        faceDir = facePath + face + "/"
        faceAmount = getFileAmount(faceDir) 
        faceFile = faceDir+str(faceAmount+1) + ".jpg"
        cv2.imwrite(faceFile,analyseFrame)
    '''
    if frameCount < amount:
       
        currFrontFrame = cv2.imread(uploadDir+str(frameCount)+".jpg")
        analyseFrame = getRtmpFrame(currFrontFrame)
        
        faceDir = facePath + face + "/"
        faceFile = faceDir+str(frameCount) + ".jpg"
        cv2.imwrite(faceFile,analyseFrame)

        faceCountArray[face] = faceCountArray[face]  + 1


def pushRtmp():
    getAnalyseFrame("front")
    getAnalyseFrame("back")
    getAnalyseFrame("left")
    getAnalyseFrame("right")
    getAnalyseFrame("top")
while True:
    pushRtmp()
