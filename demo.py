import cv2
from util import ContourUtil,TextUtil,ImgUtil,HSVFilteUtil
from roi import ROIDetect

captureFront = cv2.VideoCapture("http://192.168.1.8:8002/?action=stream")
captureLeft = cv2.VideoCapture("http://192.168.1.8:8001/?action=stream")

roiDetectLeft = ROIDetect()
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

while True:
    ret, frameFront = captureFront.read()
    ret, frameLeft = captureLeft.read()

    diffFront = roiDetectFront.getROIByDiff(frameFront)
    diffLeft = roiDetectLeft.getROIByDiff(frameLeft)

    frameFront = processImg(frameFront,diffFront)
    frameLeft = processImg(frameLeft,diffLeft)

    cv2.imshow("brickFront",frameFront)
    cv2.imshow("brickLeft",frameLeft)

    key = cv2.waitKey(1000//40)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
captureFront.release()
captureLeft.release()