import cv2
import requests
import sys
import getopt

face = ""
videourl = ""

try:
    opts,args = getopt.getopt(sys.argv[1:],"hf:v:",["face=","video="])
except getopt.GetoptError:
    print("transface.py  -f  <face> -v <video>")
    sys.exit(2)

for opt,arg in opts:
    if opt == '-h':
        print("transface.py  -f  <face> -v <video>")
        sys.exit()
    elif opt in ("-f","--face"):
        face = arg
    elif opt in ("-v","--video"):
        videourl = arg

url = "http://192.168.1.18/upload.php"
fileName = face+".jpg"
camera = cv2.VideoCapture(videourl)
while True:
    ret,frame = camera.read()
    cv2.imwrite(fileName,frame)
    files = {"file":(fileName,open(fileName,"rb"),"image/jpg",{})}
    res = requests.request("POST",url,data={"face":face},files=files)
    cv2.waitKey(25)
