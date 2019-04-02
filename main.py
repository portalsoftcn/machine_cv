
'''
正面，侧面，顶面摄像头
'''

def getFaceRotate( faceIndex ):
    rotate = 0
    if faceIndex == 0 :
        rotate = 0.1
    elif faceIndex == 1 :
        rotate = 0.2
    elif faceIndex == 2 :
        rotate = 0.3
    return rotate


###获取摄像头数据,计算某个面偏转角度
faceFront = getFaceRotate(0)
###根据偏转角度,调用硬件调整姿态
'''
升降脚
前:左(FL),右(FR);后:左(BL)右(BR)
'''
footFrontleft = "FL" 
footFrontRight = "FR"
footBackLeft = "BL"
footBackRight = "BR"



