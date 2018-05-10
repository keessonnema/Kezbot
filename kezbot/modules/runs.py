import random

from telegram.ext import run_async, CommandHandler
from kezbot.strings import run_strings

from kezbot import dispatcher


@run_async
def runs(_bot, update):
    update.effective_message.reply_text(random.choice(run_strings))


__mod_name__ = "runs"

RUNS = CommandHandler('runs', runs)
dispatcher.add_handler(RUNS)
