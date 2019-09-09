TODO APP
===========================

#### Notes
I coded this on a non-ideal machine running Windows 10 SE, 
using Bash on Ubuntu for Windows/Windows Subsystem for Linux.
As this environment is a pain to work with, I decided to write a Dockerfile
for the app and run it from there. But lo and behold, my machine isn't properly running
the HyperVisor required for Docker Desktop for Windows, and something's up with
my docker-machine's VirtualBox driver.

In any case, this should all work perfectly fine on a machine running a UNIX-like OS.

I initially misread the requirements being python 3.7, so I adjusted the previously
python2 code to work for python3. But hey, it's 2019 so why not use python3 over the
soon-to-be deprecated python2?

#### Requirements
* python 3.7
* sqlite3

#### Setup Application
* `./setup.sh`

#### Run the Application
* `./run.sh`

#### OPTIONAL: Run the application as a docker container
This is untested as my machine has issues connecting to the Virtualbox VM running
the docker-machine docker daemon. Check it out if you can though!
* ensure docker daemon is running
* `docker build -t alayacare-todo-app .`
* `docker run --rm -p 5000:5000 alayacare-todo-app`

#### Login Credentials:
* username: **user1**,  password: **user1**
* username: **user2**,  password: **user2**
* username: **user3**,  password: **user3**
