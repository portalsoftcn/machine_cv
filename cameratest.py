import cv2

camera = cv2.VideoCapture(0) 

while True:
    ret,frame = camera.read()
    resGray = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    cv2.imshow("frame",resGray)
    cv2.waitKey(40)