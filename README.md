# How to install and run europolix
tested on lubuntu 13.10 with virtualenv on March 21, 2014


## Install curl
This package let you download other packakes from the internet via a terminal.
```shell
    sudo apt-get install curl
```


## Install pip
PIP is a tool to install python software easily.
```shell
    curl -O https://pypi.python.org/packages/source/p/pip/pip-1.4.tar.gz
    tar xvfz pip-1.4.tar.gz
    cd pip-1.4
    sudo python setup.py install
```


## Install virtualenv
Virtualenv creates a virtual environment for the project. It allows you to run other projects  using the same software but with a different version.
For example this project requires python2.7, but you might need python3.0 for another project.
```shell
    pip install virtualenv
```
Create a virtual environment for europolix
```shell
    virtualenv europolix
```
Activate the environment
```shell
    source europolix/bin/activate
```
From now on, all the software will be installed under this virtual session, and available for this project only.


## Install python
Python 2.7 is the language used for this project.
```shell
    curl -O  https://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
    cd ~/Downloads
    tar zxf Python-2.7.tgz
    cd Python-2.7
    ./configure
```

If error Python.h not found:
```shell
    sudo apt-get install python-dev
```

```shell
    sudo make install
```


## Install Mysql
MySQL is the database engine used for the project.
```shell
    sudo apt-get install mysql-server
    sudo apt-get install python-setuptools python-dev build-essential
    sudo apt-get install libmysqlclient-dev
```


## Install the requirements
The file requirements.txt contains all the dependencies of the project (such as Django, Beautifulsoup). The following line is going to install them all.
```shell
    pip install -r requirements.txt
```


## Install and set up git
Git is the versionning tool used for the project. The project is currently hosted on github.
```shell
    apt-get install git
```
Inside the "europolix" website root directory (create it and move to this directory), initialize the git tracking system:
```shell
    git init
    git status
    git config --global user.name "[github username]"
    git config --global user.email "[email address]"
```
Indicate where to fetch the source code:
```shell
    git remote add origin https://github.com/EPX/epx2013.git
```
    Get the source code:
```shell
    git pull origin master
```

If you have right problems:
```shell
    sudo chown -R [username] ./
```

## Run the server (development server)
```shell
    python manage.py runserver
```

## Access the website from your webbrowser
http://127.0.0.1:8000/