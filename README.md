# rpibot
This is a simple Telegram bot that allows you to read and write GPIO logic levels of your Raspberry Pi.

## Installation
For Raspbian distro run following commands on your RPi to install required modules:
```
# aptitude update
# aptitude install -y -R git python3-pip python3-rpi.gpio

# pip3 install python-telegram-bot

# git clone https://github.com/denis-it/rpibot.git
```

## Start
```
# cd rpibot
# ./rpibot.py
```

## Known issues
If you have found any issue or have feature request - create an issue for it, please. Thanks.
