#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import logging

from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from kezbot import dispatcher, updater, token
from kezbot.config import Config
from kezbot.modules import ALL_MODULES

OWNER = int(Config.OWNER_ID)  # Telegram user ID
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
        "Hello {}. I'm Shifty. Send me a Youtube-URL and I'll give you a Spotify-URL to that song!".format
        (update.message.from_user.first_name))


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.WARNING)

    START_BOT = CommandHandler('start', start)
    dispatcher.add_handler(START_BOT)

    if Config.use_webhooks:
        cert_pem = Config.cert_pem
        webhook_url = Config.webhook_url

        updater.start_webhook(listen='127.0.0.1', port=5000, url_path=token)
        updater.bot.set_webhook(url=webhook_url + token,
                                certificate=open(cert_pem, 'rb'))
    else:
        updater.start_polling(poll_interval=1.0, timeout=20)

    updater.idle()


if __name__ == '__main__':
    main()
