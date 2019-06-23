#!/bin/sh
cd /home/pi/machine_cv/mjpg-streamer-master/mjpg-streamer-experimental/
nohup mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 " -o "output_http.so -w ./www -p 8001" &
nohup mjpg_streamer -i "input_uvc.so -d /dev/video2 -r 640x480 " -o "output_http.so -w ./www -p 8003" &
nohup mjpg_streamer -i "input_uvc.so -d /dev/video4 -r 640x480 " -o "output_http.so -w ./www -p 8005" &
nohup mjpg_streamer -i "input_uvc.so -d /dev/video6 -r 640x480 " -o "output_http.so -w ./www -p 8007" &
nohup mjpg_streamer -i "input_uvc.so -d /dev/video8 -r 640x480 " -o "output_http.so -w ./www -p 8009" &

