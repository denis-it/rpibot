#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


try:
	import RPi.GPIO as GPIO
except:
	import gpiostub as GPIO


logging.basicConfig(
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def on_start(bot, update):
	bot.sendMessage(
		chat_id=update.message.chat_id,
		text="Welcome to RPi bot starter kit.")
	on_help(bot, update)


def on_help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=
"""
Following commands are available:
/info - get information about RPi board

/high PIN - set high level on the pin
/low PIN - set low level on the pin
/get PIN - get logic level on the pin
""")


def _with_pin(bot, update, args, fn):
	try:
		result = fn(int(args[0]))
		bot.sendMessage(
			chat_id=update.message.chat_id,
			text="Ok: %s." % (result if result else "done"))
	except Exception as e:
		LOGGER.warn("command error: %s" % e)
		bot.sendMessage(chat_id=update.message.chat_id, text="Error: %s." % e)
		on_help(bot, update)


def on_info(bot, update):
	bot.sendMessage(
		chat_id=update.message.chat_id,
		text="Ok: %s." % GPIO.RPI_INFO)


def on_high(bot, update, args):
	def _handler(pin):
		GPIO.remove_event_detect(pin)
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

	_with_pin(bot, update, args, _handler)


def on_low(bot, update, args):
	def _handler(pin):
		GPIO.remove_event_detect(pin)
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	_with_pin(bot, update, args, _handler)


def on_get(bot, update, args):
	def _handler(pin):
		GPIO.setup(pin, GPIO.IN)
		result = GPIO.input(pin)
		return (result if result else "0")

	_with_pin(bot, update, args, _handler)


def on_error(bot, update, error):
	LOGGER.warn("update \"%s\" caused error \"%s\"" % (update, error))
	bot.sendMessage(chat_id=update.message.chat_id, text="Error: %s." % error)


def main():
	config = configparser.ConfigParser()
	config.read("rpibot.ini")

	GPIO.setmode(GPIO.BOARD)

	updater = Updater(token=config["GENERAL"]["token"])
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", on_start))
	dispatcher.add_handler(CommandHandler("help", on_help))
	dispatcher.add_handler(CommandHandler("info", on_info))
	dispatcher.add_handler(CommandHandler("high", on_high, pass_args=True))
	dispatcher.add_handler(CommandHandler("low", on_low, pass_args=True))
	dispatcher.add_handler(CommandHandler("get", on_get, pass_args=True))

	dispatcher.add_handler(MessageHandler(Filters.all, on_help))

	dispatcher.add_error_handler(on_error)

	updater.start_polling()
	updater.idle()

	GPIO.cleanup()


if __name__ == "__main__": main()
