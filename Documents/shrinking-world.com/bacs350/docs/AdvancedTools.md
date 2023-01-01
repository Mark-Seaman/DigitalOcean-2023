# Setup Python Environment

## Tools Install

* Linux kernel - with WSL on MS Windows OS
* Homebrew - application manager for installing tools
* pyenv - tool to manage Python Virtual Environments
* Python 3.10 - setup new Python


### Step 1 - Install Linux

The Linux shell is a great environment to execute tools.  We will need to make
sure that we have some kind of Linux-like shell to install all of the other
tools that we need.  Once we have the development tools installed we will 
continue to use this environment to work with files throughout our project.

Each operating system has its own quirks and oddities.  We will standardize
our user experience by getting to the same environment with the same set of
tools, configured the same way.


If you are running Mac OS or Linux then you can go directly to installing
Homebrew.  If you are running MS Windows then you will install WSL (Windows
Subsystem for Linux).

* [Install WSL2](https://docs.microsoft.com/en-us/windows/wsl/install)

To install WSL 2 on Windows 10 OS Build 2004 or later you need to open the
command prompt app with Administrator permissions, and enter the following
command:

    wsl.exe --install

As soon as you hit enter, the process automatically gets to work. It enables the
WSL optional features required, fetches the latest WSL Linux kernel version, and
installs Ubuntu as your default distro.  Congratulations - You now are running
Linux inside of Windows.


### Step 2 - Install Homebrew

Homebrew is an application installer to setup development tools created by
Apple.  It runs in a Linux shell and will install all of the other tools we
need.   There are many different ways to install tools.  Homebrew is a proven
way to get a common tool set across all the OS platforms.


[Install Homebrew](https://brew.sh/)

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Setup shell (copy and paste in shell)

    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.profile

    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

[Install Build tools](https://docs.brew.sh/Homebrew-on-Linux)

    sudo apt-get install build-essential

    brew install gcc

    brew doctor


### Step 3 - Install pyenv

    brew install pyenv


### Step 4 - Install Python 3.10

List the versions of Python installed

    pyenv versions

List the versions of Python available to install

    pyenv install --list

Install Python 3.10

    pyenv install 3.10.3

    pyenv global 3.10.3

Test which Python will be used

    pyenv which python

Add this in ".profile"
    
    echo 'pyenv global 3.10.3' >> ~/.profile

Restart shell

    which python


### Step 5 - Install Django

Install the django libraries into the Virtual Environment

    $ pip install django


### Step 6 - Test Django Install

Create a new Django project

    $ django-admin startproject config .

Run the web server

    $ python manage.py runserver

Browse to web page

    http://localhost:8000
    

### Step 7 - Test Your Tool Setup 

* Keep working until the page loads without errors
* No need to turn in the homework assignment.   Grades will be determined from
the content of your Github repo.
