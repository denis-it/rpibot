#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
import logging
import subprocess
import time

import RPi.GPIO as GPIO

from telegram import InlineQueryResultArticle, ChatAction, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from uuid import uuid4


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


def on_info(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=GPIO.RPI_INFO)


def on_output(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Ok.")


def on_input(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Ok.")


def on_high(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Ok.")


def on_low(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Ok.")


def on_get(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="To be implemented.")


def on_error(bot, update, error):
	logger.warn("update \"%s\" caused error \"%s\"" % (update, error))


def main():
	logging.basicConfig(
		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
		level=logging.INFO)
	logger = logging.getLogger(__name__)

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

if __name__ == "__main__": main()
