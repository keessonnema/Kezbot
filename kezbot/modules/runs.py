from random import randint
from telegram.ext import run_async, CommandHandler
from kezbot.strings import run_strings

from kezbot import dispatcher


@run_async
def runs(_bot, update):
    start_running = randint(0, len(run_strings) - 1)
    update.effective_message.reply_text(run_strings[start_running])


__mod_name__ = "Runs"

RUNS = CommandHandler('runs', runs)
dispatcher.add_handler(RUNS)
