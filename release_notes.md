#README for [ClassRank][0]

#Table of Contents

1. Release notes
2. Installation instructions
3. User manual
4. Repository information

#2 Installation instructions
Here's the basic install outline:

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

[0]: https://github.com/classrank/ClassRank
[1]: https://www.python.org
[2]: https://www.continuum.io/downloads
