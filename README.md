HOW TO INSTALL AND RUN EUROPOLIX
tested on lubuntu 13.10 with virtualenv on March 21, 2014


1/INSTALL CURL
This package let you download other packakes from the internet via a terminal.
    sudo apt-get install curl


2/INSTALL PIP
PIP is a tool to install python software easily.
    curl -O https://pypi.python.org/packages/source/p/pip/pip-1.4.tar.gz
    tar xvfz pip-1.4.tar.gz
    cd pip-1.4
    sudo python setup.py install


3/INSTALL VIRTUALENV
Virtualenv creates a virtual environment for the project. It allows you to run other projects  using the same software but with a different version.
For example this project requires python2.7, but you might need python3.0 for another project.
    pip install virtualenv
Create a virtual environment for europolix
    virtualenv europolix
Activate the environment
    source europolix/bin/activate
From now on, all the software will be installed under this virtual session, and available for this project only.


4/INSTALL PYTHON
Python 2.7 is the language used for this project.
    curl -O  https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
    cd ~/Downloads
    tar zxf Python-2.7.tgz
    cd Python-2.7
    ./configure

If error Python.h not found:
sudo apt-get install python-dev

    sudo make install


5/INSTALL MYSQL
MySQL is the database engine used for the project.
    sudo apt-get install mysql-server
    sudo apt-get install python-setuptools python-dev build-essential
    sudo apt-get install libmysqlclient-dev


6/INSTALL THE REQUIREMENTS
The file requirements.txt contains all the dependencies of the project (such as Django, Beautifulsoup). The following line is going to install them all.
    pip install -r requirements.txt


7/INSTALL AND SET UP GIT
Git is the versionning tool used for the project. The project is currently hosted on github.
    apt-get install git
Inside the "europolix" website root directory (create it and move to this directory), initialize the git tracking system:
    git init
    git status
    git config --global user.name "[github username]"
    git config --global user.email "[email address]"
Indicate where to fetch the source code:
    git remote add origin https://github.com/EPX/epx2013.git
    Get the source code:
    git pull origin master

If you have right problems:
    sudo chown -R [username] ./


8/RUN THE SERVER (development server)
    python manage.py runserver


9/ACCESS IT FROM A WEB BROWSER
http://127.0.0.1:8000/