import cv2
import numpy as np
from machine import Arduino
from brickface import BrickFace
from matplotlib import pyplot as plt

'''
摄像头:
正面(Front)，右面(Right)，顶面(Top)

升降脚:
前:左(FL),右(FR);后:左(BL)右(BR)

根据偏转角度,调用硬件调整姿态
前面:左低(FL,BL),右低(FR,BR)
右面:左低(FL,FR),右低(BL,BR)
'''

footFrontleft = "FL" 
footFrontRight = "FR"
footBackLeft = "BL"
footBackRight = "BR"

###获取摄像头数据,计算某个面偏转角度
frontCamera = BrickFace(BrickFace.frontFace)
rightCamera = BrickFace(BrickFace.rightFace)

while True:
    
    frontRotate,frontFrame = frontCamera.getFaceState()
    cv2.waitKey(20)
    rightRotate,rightFrame = rightCamera.getFaceState()
    cv2.waitKey(20)
    
    frame = np.hstack( (frontFrame,rightFrame) )

    cv2.imshow("BrickFaces",frame)
    
    '''
    plt.subplot(121),plt.imshow(frontFrame)
    plt.title("Front"),plt.xticks([]),plt.yticks([])

    plt.subplot(122),plt.imshow(rightFrame)
    plt.title("Right"),plt.xticks([]),plt.yticks([])
    
    plt.show() 
    
    
    
    
    cv2.imshow("Right",rightFrame)
    '''
    







