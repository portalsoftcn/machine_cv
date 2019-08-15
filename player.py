from tkinter import *
from PIL import Image, ImageTk,ImageFile
from io import BytesIO
import base64
import redis
import time

get_now_milli_time = lambda:int( time.time() * 1000 )
red = redis.Redis(host='localhost', port=6379)
waitTime = 1
count = ""
show_before = 0
show_after = 0

labelDict = {}

def showFaces():
    global show_before
    global show_after
    global count
    show_before = get_now_milli_time()
    count = bytes.decode(red.get('count'))

    faceKeys = labelDict.keys()

    for face in faceKeys:
        updateFace(face,labelDict[face])
        fileName = face + "/" + str(int(count)-1) + ".jpg"
        red.delete(fileName)
        time.sleep(0.001)

    show_after = get_now_milli_time()

    print("show use:"+str(show_after - show_before))
    topLabel.after(waitTime,showFaces)

def updateFace(face,faceLabel):
    fileName = face + "/" + count + ".jpg"
    base64_data = red.get(fileName)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    faceImg = ImageTk.PhotoImage(img)
    faceLabel.config(image = faceImg)
    faceLabel.image = faceImg


root = Tk()
root.title('Auto Machine')

topLabel = Label(root)
topLabel.grid(row=0,column=1)

leftLabel = Label(root)
leftLabel.grid(row=1,column=0)

frontLabel = Label(root)
frontLabel.grid(row=1,column=1)

rightLabel = Label(root)
rightLabel.grid(row=1,column=2)

backLabel = Label(root)
backLabel.grid(row=2,column=1)

labelDict = {"front":frontLabel,"back":backLabel,"left":leftLabel,"right":rightLabel,"top":topLabel}

topLabel.after(waitTime,showFaces)
'''
leftLabel.after(waitTime,showLeftImg)
frontLabel.after(waitTime,showFrontImg)
rightLabel.after(waitTime,showRightImg)
backLabel.after(waitTime,showBackImg)
'''

mainloop()

