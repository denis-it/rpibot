FROM python:3.6

MAINTAINER Denis T. <dev@denis-it.com>

WORKDIR /usr/src/rpibot

RUN pip install python-telegram-bot --upgrade

COPY . .

ENTRYPOINT ["python3"]
