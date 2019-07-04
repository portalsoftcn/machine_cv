#!/bin/sh
nohup mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 " -o "output_http.so -w ./www -p 8001"&
nohup mjpg_streamer -i "input_uvc.so -d /dev/video2 -r 640x480 " -o "output_http.so -w ./www -p 8003"&
nohup mjpg_streamer -i "input_uvc.so -d /dev/video4 -r 640x480 " -o "output_http.so -w ./www -p 8005"&

