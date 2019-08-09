import redis
import cv2
import time

red = redis.Redis(host='localhost', port=6379)
get_now_milli_time = lambda:int( time.time() * 1000 )
while True:
    read_before = get_now_milli_time()
    cv2.waitKey(1)
    count = red.get('count')
    read_after = get_now_milli_time()

    print("count is:"+str(count)+" read use:"+str(read_after - read_before))