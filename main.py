import cv2
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

faceType = camerastate.CameraState.rightFace
camera = camerastate.CameraState(faceType)

#print("faceType:",faceType,"Rotate:",rotate)

while True:
    rotate,frame = camera.getFaceState()
    text = 'rotate:%.1f'%rotate
    org = 40,80
    fontFace = cv2.FONT_HERSHEY_COMPLEX
    fontScale = 1
    fontColor = (0,0,255)
    thickness = 1
    lintType = 4
    bottomLeftOrigin = 1
    cv2.putText(frame,text,org,fontFace,fontScale,fontColor,thickness,lintType)    
    cv2.imshow(faceType,frame)
    cv2.waitKey(25)

arduino = machine.Arduino()
arduino.sendCmd(50)






