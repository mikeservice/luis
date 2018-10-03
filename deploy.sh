#!/bin/bash

# Author : Alexis Richard
# Copyright (c) email_hunter.alexis
# Jan 27 2018

echo "Installing Python dependencies..."
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx

echo "Installing virtualenv pip..."
sudo pip3 install virtualenv

echo "Creating virtualenv. The path will be $HOME/Environments/coupon/"
mkdir Environments
cd Environments/
virtualenv coupon
source coupon/bin/activate


cd /var/
sudo chown ubuntu:www-data www/ -R

cd www/
git clone git@github.com:puma10/coupon_scraper.git
sudo chown ubuntu:www-data coupon_scraper/ -R

cd coupon_scraper/
git checkout dev

pip install -r requirements.txt


deactivate
cd ~
sudo apt-get install postgresql postgresql-contrib

export FLASK_APP=run.py
export FLASK_CONFIG=staging
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app


sudo nano /etc/systemd/system/coupon_scraper.service
sudo systemctl start coupon_scraper.service
sudo systemctl enable coupon_scraper.service



sudo ln -s /etc/nginx/sites-available/coupon_scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx.service
sudo service nginx restart

sudo mkdir /var/log/uwsgi
sudo chown ubuntu:ubuntu /var/log/uwsgi/ -R

source ~/Environments/coupon/bin/activate
flask db current
sudo systemctl restart coupon_scraper.service
sudo service nginx restart



sudo apt-get update
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt-get install nodejs

cd /var/www/coupon_scraper/
npm install
sudo apt-get install build-essential
npm run build


echo "Installing redis server..."
sudo apt-get update
sudo apt-get install build-essential tcl
cd /tmp/
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make
make test
sudo make install

sudo mkdir /etc/redis
sudo cp /tmp/redis-stable/redis.conf /etc/redis/
sudo nano /etc/redis/redis.conf
# Change config file
# supervised systemd
# dir /var/lib/redis

sudo nano /etc/systemd/system/redis.service
sudo adduser --system --group --no-create-home redis
sudo mkdir /var/lib/redis
sudo chown redis:redis /var/lib/redis/
sudo chmod 700 /var/lib/redis/
sudo systemctl start redis.service
sudo systemctl status redis

sudo systemctl enable redis.service


echo "Installing chrome driver and xvfb"
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
sudo apt-get install -f
sudo apt-get update
sudo apt-get install xvfb


echo "Creating swap storage"

df -h
sudo fallocate -l 2G /swapfile
ls -lh /swapfile
sudo chmod 600 /swapfile
ls -lh /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
free -h




sudo nano /etc/init.d/celeryd
sudo chmod 755 /etc/init.d/celeryd
sudo chown ubuntu:root /etc/init.d/celeryd

cd /var/log/
sudo mkdir coupon_scraper
sudo chown ubuntu:www-data coupon_scraper/
cd /var/log/coupon_scraper/
mkdir celery


sudo chown root /etc/default/celeryd
sudo /etc/init.d/celeryd start








celery worker -A src.apps.celery --loglevel=info -P eventlet --concurrency 3






sudo chmod +x chromedriver_linux





ps -Af | grep chrome



watch -n 5 free -m



sudo apt-get remove google-chrome-stable


wget https://www.slimjet.com/chrome/download-chrome.php?file=lnx%2Fchrome64_61.0.3163.79.deb

sudo dpkg -i download-chrome.php\?file\=lnx%2Fchrome64_61.0.3163.79.deb


sudo apt-get install google-chrome-stable









echo "Installing supervisor"
sudo apt-get install -y supervisor
pip install supervisor==3.3.3