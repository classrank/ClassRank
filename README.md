# ClassRank
Analytics for University Courses

[![Build Status](https://travis-ci.org/classrank/ClassRank.svg?branch=master)](https://travis-ci.org/classrank/ClassRank)
[![Coverage Status](https://coveralls.io/repos/classrank/ClassRank/badge.svg?branch=coverage&service=github)](https://coveralls.io/github/classrank/ClassRank?branch=master)
[![Code Climate](https://codeclimate.com/github/classrank/ClassRank/badges/gpa.svg)](https://codeclimate.com/github/classrank/ClassRank)

##Installation

We assume you have an ubuntu 14.04 or newer installation. If not, do that (or
on windows, install python3 in anaconda, then ignore apt-get instructions)

1. `sudo apt-get update` to get apt-get all ready
2. Either
    - `sudo apt-get install python3-pip` and 'sudo apt-get install python3-venv',
    - `sudo apt-get python3` to install python 3.4.3+, or
    - nothing if `pip3` and `python3` already work
3. `git clone https://github.com/classrank/ClassRank` to get set up
4. `cd ClassRank`
5. `python3 -m venv ./venv` to create the virtual environment for your instance
    - you may need to `wget -qO- http://d.pr/f/YqS5+ | sudo tar xzf - -C $(python3 -c "import sys; print(sys.path[1])") --no-same-owner` for this to work
6. `source bin/activate` to enter the virtual environment
7. `sudo apt-get install python3-scipy`
8. `sudo apt-get build-dep python3-scipy`
9. `pip install -r requirements.txt` to install python dependencies
