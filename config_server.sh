#!/bin/bash
yum update
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite sqlite-devel 
yum install -y readline-devel tk tk-devel gdbm gdbm-devel db4-devel libpcap-devel lzma xz xz-devel libuuid-devel libffi-devel
yum install -y emacs git
tar -zxvf Python-3.7.3.tgz
cd Python-3.7.3
./configure --prefix=/usr/local/python3
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
pip3 install pip --upgrade
pip3 install opencv-python
cd /home/machine_cv
python3 live.py


