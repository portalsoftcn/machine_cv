#!/bin/bash
yum update -y
yum install -y zlib zlib-devel bzip2-devel openssl openssl-devel ncurses-devel sqlite sqlite-devel 
yum install -y readline-devel tk tk-devel gdbm gdbm-devel db4-devel libpcap-devel lzma xz xz-devel libuuid-devel libffi-devel
yum install -y gcc gcc-c++ pcre pcre-devel zlib epel-release
yum install -y emacs
tar -zxvf Python-3.7.3.tgz
cd Python-3.7.3
./configure --prefix=/usr/local/python3
make && make install
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
pip3 install pip --upgrade
pip3 install opencv-python
pip3 install scipy
cd /home/machine_cv
tar -zxvf nginx-1.17.1.tar.gz
mv nginx-rtmp-module nginx-1.17.1
cd nginx-1.17.1
./configure --prefix=/usr/local/nginx --add-module=nginx-rtmp-module  --with-http_ssl_module
make && make install
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
yum install ffmpeg ffmpeg-devel -y
