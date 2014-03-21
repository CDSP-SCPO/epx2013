HOW TO INSTALL AND RUN EUROPOLIX
tested on lubuntu 13.10 with virtualenv on March 21, 2014


1/INSTALL PYTHON
download python from https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
cd ~/Downloads
tar zxf Python-2.7.tgz
cd Python-2.7
./configure

if error Python.h not found:
sudo apt-get install python-dev

sudo make install


2/INSTALL PIP
sudo apt-get install curl
curl -O https://pypi.python.org/packages/source/p/pip/pip-1.4.tar.gz
tar xvfz pip-1.4.tar.gz
cd pip-1.4
sudo python setup.py install


3/INSTALL MYSQL
sudo apt-get install mysql-server
sudo apt-get install python-setuptools python-dev build-essential
sudo apt-get install libmysqlclient-dev


4/INSTALL THE REQUIREMENTS
pip install -r requirements.txt


5/RUN THE SERVER (development server)
python manage.py runserver


6/ACCESS IT FROM A WEB BROWSER
http://127.0.0.1:8000/