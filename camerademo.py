import cv2

camera1 = cv2.VideoCapture(0) # 从文件读取视频
camera2 = cv2.VideoCapture(1) # 从文件读取视频
camera3 = cv2.VideoCapture(2) # 从文件读取视频
    #这里的摄像头可以在树莓派3b上使用
'''
if (camera.isOpened()):# 判断视频是否打开 
    print ('Open camera')
else:
    print ('Fail to open camera!')
'''
while True:
    ret1,frame1 = camera1.read()
    ret2,frame2 = camera2.read()
    ret3,frame3 = camera3.read()

    cv2.imshow("frame",frame1)
    cv2.imshow("frame",frame2)
    cv2.imshow("frame",frame3)

    cv2.waitKey(40)
