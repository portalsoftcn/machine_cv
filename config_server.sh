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
cd ..
tar -zxvf nginx-1.17.1.tar.gz
cd nginx-1.17.1
./configure --prefix=/usr/local/nginx  --with-http_ssl_module
make && make install
mv /root/machine_cv /usr/local/nginx/html
cp /usr/local/nginx/html/machine_cv/nginx.conf /usr/local/nginx/conf
cd /usr/local/nginx/html/machine_cv
chmod +777 web/ -R
cd /usr/local/nginx/sbin
./nginx -t
./nginx
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
yum install php72w.x86_64 php72w-fpm.x86_64 php72w-cli.x86_64 php72w-common.x86_64 php72w-gd.x86_64 php72w-ldap.x86_64 php72w-mbstring.x86_64 php72w-mcrypt.x86_64 php72w-mysqlnd.x86_64 php72w-pdo.x86_64 php72w-pecl-redis.x86_64 php72w-opcache.x86_64 php72w-devel.x86_64 php72w-bcmath.x86_64 -y
systemctl start php-fpm
systemctl enable php-fpm
