from telegram.ext import run_async, CommandHandler
from kezbot import dispatcher


@run_async
def get_id(_bot, update):
    sender = update.message.from_user
    sender_id = str(sender.id)
    update.effective_message.reply_text("Your ID is " + sender_id)


GET_ID = CommandHandler("id", get_id)
dispatcher.add_handler(GET_ID)
