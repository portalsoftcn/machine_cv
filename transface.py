import cv2
import requests
import sys
import getopt

face = ""
videourl = ""
serverip = ""

try:
    opts, args = getopt.getopt(sys.argv[1:], "-h-f:-v:-s:", ["face=", "video=","server="])
except getopt.GetoptError:
    print("transface.py  -f <face> -v <video>  -s<server>")
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print("transface.py -f <face> -v<video> -s<server>")
        sys.exit()
    elif opt in ("-f", "--face"):
        face = arg
    elif opt in ("-v", "--video"):
        videourl = arg
    elif opt in ("-s","--server"):
        serverip = arg

url = "http://"+serverip+"/upload.php"
fileName = face+".jpg"
camera = cv2.VideoCapture(videourl)
while True:
    ret, frame = camera.read()
    cv2.imwrite(fileName, frame)
    files = {"file": (fileName, open(fileName, "rb"), "image/jpg", {})}
    res = requests.request("POST", url, data={"face": face}, files=files)
    cv2.waitKey(25)
    print(serverip + face + "trans success")