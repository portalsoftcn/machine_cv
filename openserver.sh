#!/bin/bash
cd /usr/local/src/nginx/sbin
sudo ./nginx
cd /home/pi/machine_cv/
python3 live.py
