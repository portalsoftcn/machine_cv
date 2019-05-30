import cv2
import numpy as np
from scipy import ndimage
from util import ContourUtil,TextUtil,ImgUtil
from matplotlib import pyplot as plt
from roi import ROIDetect


imgPath = "roi3.jpg"

brickImg = cv2.imread(imgPath)

brickImgGray = cv2.cvtColor(brickImg, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(
    brickImgGray, 150, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imshow("gray",brickImgGray)
cv2.imshow("thresh",thresh)

kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

sure_bg = cv2.dilate(opening, kernel, iterations=3)

dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

ret, sure_fg = cv2.threshold(
    dist_transform, 0.4 * dist_transform.max(), 255, 0)

sure_fg = np.uint8(sure_fg)

unknown = cv2.subtract(sure_bg, sure_fg)

ret, markers = cv2.connectedComponents(sure_fg)

markers = markers + 1
markers[unknown == 255] = 0

markers = cv2.watershed(brickImg, markers)

brickImg[markers == -1] = [255, 0, 0]

cv2.imshow("brick",brickImg)

cv2.waitKey()
cv2.destroyAllWindows()