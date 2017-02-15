FROM python:3.4.6

MAINTAINER Denis T. <dev@denis-it.com>

WORKDIR /usr/src/rpibot

RUN pip install telepot \
	&& pip install telepot --upgrade

ENV PYTHONUNBUFFERED 1

COPY . .

ENTRYPOINT ["python3"]
