import cv2

camera = cv2.VideoCapture(1) # 从文件读取视频
    #这里的摄像头可以在树莓派3b上使用
if (camera.isOpened()):# 判断视频是否打开 
    print ('Open camera')
else:
    print ('Fail to open camera!')
while True:
    ret,frame = camera.read()
    cv2.imshow("frame",frame)
    cv2.waitKey(40)
