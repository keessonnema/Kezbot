#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging

from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from kezbot import dispatcher, updater, TOKEN
from kezbot.config import Config
from kezbot.modules import ALL_MODULES

OWNER = int(Config.OWNER_ID)
IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("kezbot.modules." + module_name)

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")


@run_async
def start(_bot, update):
    update.effective_message.reply_text(
        "Hi {}, I'm Shifty! I can easily help you switch between Youtube and Spotify."
        " Just give me a link to a song!".format
        (update.message.from_user.first_name))


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

    START_BOT = CommandHandler('start', start)
    dispatcher.add_handler(START_BOT)

    if Config.USE_WEBHOOKS:
        CERT_PEM = Config.CERT_PEM
        WEBHOOK_URL = Config.WEBHOOK_URL
        updater.start_webhook(listen='127.0.0.1', port=5001, url_path=TOKEN)
        updater.bot.set_webhook(url=WEBHOOK_URL + TOKEN, certificate=open(CERT_PEM, 'rb'))
    else:
        updater.start_polling(poll_interval=1.0, timeout=20)

    updater.idle()


if __name__ == '__main__':
    main()
