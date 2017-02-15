# rpibot
This is a simple Telegram bot that allows you to read and write GPIO logic levels of your Raspberry Pi.

## Installation
For Raspbian distro run following commands on your RPi to install required modules:
```
$ sudo aptitude update
$ sudo aptitude install -y -R git python3-pip python3-rpi.gpio

$ sudo pip3 install python-telegram-bot

$ git clone https://github.com/denis-it/rpibot.git
$ cd rpibot
```

## Configuration
1. Copy `rpibot.ini_sample` to `rpibot.ini`.
1. Paste your [telegram bot token](https://core.telegram.org/bots#3-how-do-i-create-a-bot) in place of `YOUR_TOKEN_HERE` string.
```
$ cp rpibot.ini_sample rpibot.ini
$ editor rpibot.ini
```
## Start
Just run `rpibot.py` script:
```
$ ./rpibot.py
```

## Known issues
If you have found a bug or have a feature request - create an issue for it, please. Thanks.
