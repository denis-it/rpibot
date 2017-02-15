#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


try:
	import RPi.GPIO as GPIO
except:
	class GPIOStub(object):
		def __init__(self): self.BOARD = self.IN = self.OUT =self.RPI_INFO = "STUB"
		def setmode(self, mode): pass
		def setup(self, pin, direction): pass
		def output(self, pin, level): pass
		def input(self, pin): pass
		def cleanup(self): pass
	GPIO = GPIOStub()


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

/output PIN - configure GPIO pin as output
/input PIN - configure GPIO pin as input

/high PIN - set high level on the pin
/low PIN - set low level on the pin
/get PIN - get logic level on the pin
""")


def _with_pin(bot, update, args, fn):
	try:
		result = fn(args[0])
		bot.sendMessage(chat_id=update.message.chat_id, text="Ok.")
		return result
	except Exception as e:
		LOGGER.warn("command error: %s" % e)
		bot.sendMessage(chat_id=update.message.chat_id, text="Error: %s." % e)
		on_help(bot, update)


def on_info(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=GPIO.RPI_INFO)


def on_output(bot, update, args):
	_with_pin(bot, update, args, lambda pin: GPIO.setup(pin, GPIO.OUT))


def on_input(bot, update, args):
	_with_pin(bot, update, args, lambda pin: GPIO.setup(pin, GPIO.IN))


def on_high(bot, update, args):
	_with_pin(bot, update, args, lambda pin: GPIO.output(pin, True))


def on_low(bot, update, args):
	_with_pin(bot, update, args, lambda pin: GPIO.output(pin, False))


def on_get(bot, update, args):
	_with_pin(bot, update, args, lambda pin: GPIO.input(pin))


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
	dispatcher.add_handler(CommandHandler("output", on_output, pass_args=True))
	dispatcher.add_handler(CommandHandler("input", on_input, pass_args=True))
	dispatcher.add_handler(CommandHandler("high", on_high, pass_args=True))
	dispatcher.add_handler(CommandHandler("low", on_low, pass_args=True))
	dispatcher.add_handler(CommandHandler("get", on_get, pass_args=True))

	dispatcher.add_handler(MessageHandler(Filters.all, on_help))

	dispatcher.add_error_handler(on_error)

	updater.start_polling()
	updater.idle()

	GPIO.cleanup()


if __name__ == "__main__": main()
