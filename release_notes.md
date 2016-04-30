#README for [ClassRank][0]

#Table of Contents

1. Release notes
2. Installation Instructions
3. User manual
4. Repository information

#1 Release Notes

 - Version Number: 1.0.0
 - Status: Beta Release
 - Known Bugs:
    - Default settings have the system in debug mode by default, this leads to
      security vulnerabilities 
    - Certain pages do not have complete error handling so they fall into
      the debug output and do not use in-application handling
    - There are some unimplemented pages (professor view, privacy policy, etc.)
    - There will be numerical instabilities with a large number of users due
      to a missing bounds check in the code that decides the number of latent
      factors


#2 Installation Instructions

Here is the basic install outline:

1. install Python2, Python3, and the dependencies of ClassRank
2. run a script that installs Grouch, runs Grouch, and deletes Grouch
3. start up the server

Steps 2 and 3 will take a while to run, and step 2 requires you run the
script on a bash-enabled machine (best to run on a Unix-like [linux, OSX]).

##2.1 Installing Python and dependencies

1. install python2 and python3 (either from the [official website][1] or with
   your package manager of choice)
2. install pip for both python2 and python3 (may already be there from step 1)
3. install virtualenv for python2: `pip2 install virtualenv`
4. download ClassRank: `git clone https://github.com/classrank/ClassRank`
5. enter the ClassRank directory: `cd ClassRank`
6. create the virtual environment: `python3 -m venv .`
7. activate your virtual environment: `source bin/activate`
8. install scipy
    - if on ubuntu: `sudo apt-get install python3-scipy`,
      `sudo apt-get build-dep python3-scipy`
    - if on Windows, use [Anaconda][2]
    - if on Mac, you can use Homebrew to install scipy
      `brew install homebrew/python/scipy`. If this fails to work, you can also
       use Anaconda
9. install the rest of the dependencies: `pip install -r requirements.txt`

##2.2 Installing, Running, and Deleting Grouch

1. run the following command (note, this will take approximate ~10 minutes):
   `bash classrank/grouch/run_grouch.sh`

##2.3 Starting the server
Note: if you want to tweak the server settings to your liking, create a file
`config.json`, and have classrank.py look to it for settings. See
`config.json.example` for an example document. For exploratory running of the
server, this is not necessary.

1. run the following commans (note, this will take approximately ~5 minutes):
   `python3 classrank.py`

After the server tells you "Database import complete" (or something along those
lines), navigate to localhost:8000, and see ClassRank go.

#3 User Guide

Once the application is live, you can visit it in a web browser. Do so, then
register an account and log in. After that, rate courses on the course rate
screen, and view predictions based on the ratings made by other users.

#4 Repository Information
[ClassRank](https://github.com/classrank/ClassRank) and
[Grouch](https://github.com/classrank/Grouch)

Note: our 1.0 release is [here](https://github.com/classrank/ClassRank/releases/tag/v1.0)
. This is our official 1.0 release, and the
project, for the intents of this course, is 'done'. However,
we will continue working beyond it. So, grade from there. Or, grade from where
we are at the time of grading. Your choice.

[0]: https://github.com/classrank/ClassRank
[1]: https://www.python.org
[2]: https://www.continuum.io/downloads
