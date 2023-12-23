#!/bin/bash

if [ ! -f .env ]
then
    echo ".env file not found. Aborting"
    exit 2
fi

if [ ! -d text ]
then
    echo "Creating directory ./text"
    mkdir text
fi

if [ ! -d voice ]
then
    echo "Creating directory ./voice"
    mkdir voice
fi

if [ ! -d dejavu-fonts-ttf-2.37 ]
then
    echo "Downloading the fonts..."
    wget https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip
    unzip ./dejavu-fonts-ttf-2.37.zip
    rm -f ./dejavu-fonts-ttf-2.37.zip
fi

pip install -r requirements.txt
python __main__.py