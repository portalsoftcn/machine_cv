import machine
import camerastate

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

faceType = camerastate.CameraState.frontFace
camera = camerastate.CameraState(faceType)
rotate,facePic = camera.getFaceState()

print("faceType:",faceType,"Rotate:",rotate)

arduino = machine.Arduino()
arduino.sendCmd(50)






