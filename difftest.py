import cv2
import numpy as np
from scipy import ndimage

capture = cv2.VideoCapture(0)
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
background = None

while True:
    ret, frame = capture.read()
    if background is None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (11, 11), 0)
        continue
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (11, 11), 0)

    diff = cv2.absdiff(background, gray_frame)
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)
    cnts, hierarchy = cv2.findContours(
        diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rotate = 0
    maxCnt = None
    for cnt in cnts:
        if (maxCnt is None) or cv2.contourArea(cnt) >= cv2.contourArea(maxCnt):
            maxCnt = cnt
    if not maxCnt is None:
        x, y, w, h = cv2.boundingRect(maxCnt)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        minRect = cv2.minAreaRect(maxCnt)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        rotate = minRect[2]
        box = cv2.boxPoints(minRect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0, 0, 255), 1)

    text = " rotate: %.1f" % rotate
    org = 40, 80
    fontFace = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    fontColor = (0, 0, 255)
    thickness = 1
    lintType = 4
    bottomLeftOrigin = 1
    cv2.putText(frame, text, org, fontFace, fontScale,
                fontColor, thickness, lintType)
    cv2.imshow("contours", frame)
    if cv2.waitKey(1000//25) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
capture.release()
