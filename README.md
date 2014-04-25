# How to install and run europolix
tested on lubuntu 13.10 with virtualenv on March 21, 2014


## Create the directory of the project
Go to the directory of your choice in a terminal and type:

```shell
    mkdir europolix
    cd europolix
```


## Install and set up git
Git is the versionning tool used for the project. The project is currently hosted on github.
```shell
    sudo apt-get install git
```

Initialize the git tracking system:

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


## Get the source code
Fetch the source code from the github directory and copy it inside the root directory of the project

```shell
    git pull origin master
```

If you have right problems:

```shell
    sudo chown -R [username] ./
```


## Install Mysql
MySQL is the database engine used for the project.

```shell
    sudo apt-get install mysql-server python-setuptools python-dev build-essential libmysqlclient-dev
```

## Connect the database on your server
Copy the sql file of the original database on your local machine (using scp for example).
Create a database called `europolix` from the mysql interpreter:

```shell
    mysql -u root -p
    CREATE SCHEMA `europolix` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
    exit;
```

Create the tables from the sql file.

```shell
    mysql -u root -p europolix < [/path/sql/file]
```


## Update the settings file
Inside the europolix directory, update the settings.py file.
At the beginning, modify `WEB_ROOT` to point to the address of your server.
In the `DATABASES` section, update `USER` and `PASSWORD` to correspond to your mysql ids.



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





## Install curl
This package let you download other packakes from the internet via a terminal.

```shell
    sudo apt-get install curl
```

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

Then finish the installation of python

```shell
    sudo make install
```


## Install pip
PIP is a tool to install python software easily.

```shell
    curl -O https://pypi.python.org/packages/source/p/pip/pip-1.4.tar.gz
    tar xvfz pip-1.4.tar.gz
    cd pip-1.4
    sudo python setup.py install
```



## Install the requirements
The file requirements.txt contains all the dependencies of the project (such as Django, Beautifulsoup). The following line is going to install them all.

```shell
    pip install -r requirements.txt
```



## Run the server (development server)

```shell
    python manage.py runserver
```

## Access the website from your web browser
http://127.0.0.1:8000/
