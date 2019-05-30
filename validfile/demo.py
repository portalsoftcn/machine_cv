import cv2
import numpy as np
from scipy import ndimage
import sys
from matplotlib import pyplot as plt

blue = np.zeros((256,256),dtype = np.uint8)
blue = cv2.cvtColor(blue,cv2.COLOR_GRAY2BGR)


maxIndex  = 256
for row in range(0,maxIndex):
    for col in range(0,maxIndex):
        #print("row-col:",row,col)
        blue[row,col] = [255,min(row,150),min(col,120)]
blueHsv = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)

cv2.imwrite("filtebg/bg.jpg",blue)

cv2.imshow("blue", blue)
cv2.imshow("blueHsv", blueHsv)

#cv2.imshow("hsv", bgHsv)
cv2.waitKey()
cv2.destroyAllWindows()
