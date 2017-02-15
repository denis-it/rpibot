#!/bin/bash

aptitude update
aptitude install -y -R git python3-pip python3-rpi.gpio

pip3 install python-telegram-bot

git clone https://github.com/denis-it/rpibot.git
