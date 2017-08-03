#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import configparser
import requests
import strings
import os
import time
import sys
import logging
import spotipy
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


#basic commands for the bot

owner_id = int(Config.OWNER_ID)


def start(bot, update):
    update.effective_message.reply_text("Hello {}. I'm KezBot. What can I do for you?".format(update.message.from_user.first_name))


def hello(bot, update):
    update.effective_message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def simao(bot, update):
    update.effective_message.reply_text("He sucks at just about everything!")


def hardtraxx(bot, update):
    update.effective_message.reply_text("Hardstylboy was here!!!")


def ip(bot, update):
    sender = update.message.from_user

    if sender.id == owner_id:
        res = requests.get("http://ipinfo.io/ip")
        ip = res.text
        update.effective_message.reply_text("The server's IP is " + ip)
    else:
        update.effective_message.reply_text(strings.stringAdminOnly)


def getid(bot, update):
    sender = update.message.from_user

    sender_id = str(sender.id)

    update.effective_message.reply_text("Your ID is " + sender_id)


def main():

    token = Config.API_KEY
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('simao', simao))
    updater.dispatcher.add_handler(CommandHandler('hardtraxx', hardtraxx))
    updater.dispatcher.add_handler(CommandHandler("ip", ip))
    updater.dispatcher.add_handler(CommandHandler("id", getid))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()