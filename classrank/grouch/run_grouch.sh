#!/usr/bin/env bash

set -e

INSTALL=1    # 1: install grouch; use 0 if already installed
CLEANCYCLE=1 # 1: remove installed grouch; use 0 if you want to keep it

RESULT_FILE='result.json'

if [ $INSTALL -eq 1 ]
then
    git clone --depth=1 https://github.com/classrank/Grouch.git grouch_install
    rm -rf !$/.git
    cd grouch_install
    python2 -m pip install virtualenv
    python2 -m virtualenv venv
    source venv/bin/activate
    python2 -m pip install scrapy
    deactivate
    cd ..
fi

cd grouch_install
source venv/bin/activate
scrapy crawl -o $RESULT_FILE -t json oscar
cp $RESULT_FILE ..
cd ..

if [ $CLEANCYCLE -eq 1 ]
then
    rm -rf grouch_install
fi
