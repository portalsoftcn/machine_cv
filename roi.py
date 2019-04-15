import cv2
import numpy as np
from scipy import ndimage
from util import ContourUtil,TextUtil
from matplotlib import pyplot as plt

class ROIDetect:

    _es = None
    _contourUtil = None

    def __init__(self):
        self._es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        self._contourUtil = ContourUtil()
    
    def getROIContour(self,bgImg,currImg):
        

        gray_frame = cv2.cvtColor(currImg, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (11, 11), 0)

        diff = cv2.absdiff(bgImg, gray_frame)
        diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        diff = cv2.dilate(diff, self._es, iterations=2)

        maxCnt = self._contourUtil.getMaxContour(diff.copy())
        
        return maxCnt