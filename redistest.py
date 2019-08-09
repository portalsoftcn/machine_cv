import cv2
import time
import requests

get_now_milli_time = lambda:int( time.time() * 1000 )
while True:
    read_before = get_now_milli_time()
    time.sleep(0.01)

    count_url = "http://localhost:8080/countfileserv"
    response = requests.get(count_url)

    read_after = get_now_milli_time()

    print("count is:"+response.text+" read use:"+str(read_after - read_before))