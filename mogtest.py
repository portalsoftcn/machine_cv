import cv2
import numpy as np
        
capture = cv2.VideoCapture(0)
mog = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = capture.read()
    fgmask = mog.apply(frame)
    cv2.imshow("frame",fgmask)
    if cv2.waitKey(40) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
capture.release()
