import redis
import base64
import time


red = redis.Redis(host='localhost', port=6379)
get_now_milli_time = lambda:int( time.time() * 1000 )

faceIndex = 1

while faceIndex < 14939:
    read_before = get_now_milli_time()
    with open("web/faceimg/front/"+str(faceIndex)+".jpg","rb") as f:#转为二进制格式
        base64_data = base64.b64encode(f.read())#使用base64进行加密
        red.set("front/"+str(faceIndex)+".jpg",base64_data)
    read_after = get_now_milli_time()
    print(str(faceIndex)+" read use:"+str(read_after - read_before))
    faceIndex = faceIndex + 1
