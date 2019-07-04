#!/bin/bash
yum update
yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite sqlite-devel 
yum install -y readline-devel tk tk-devel gdbm gdbm-devel db4-devel libpcap-devel lzma xz xz-devel libuuid-devel libffi-devel
yum install -y emacs git
cd /home
git clone https://gitee.com/lvchenghui/machine_cv.git
cd machine_cv
tar -zxvf Python-3.7.3.tgz
cd Python-3.7.3
./configure --prefix=/usr/local/python3

