#!/bin/sh
cd /home/pi/mjpg-streamer-master/mjpg-streamer-experimental/
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video0 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8001" &
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video1 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8002" &
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video2 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8003" &
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video3 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8004" &
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video4 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8005" &
nohup ./mjpg_streamer -i "input_uvc.so -y -d /dev/video5 -r 640x480 -f 30" -o "output_http.so -w ./www -p 8006" &

