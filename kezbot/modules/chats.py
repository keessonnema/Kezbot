from time import sleep

import sys
import telegram
from telegram import TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters

from database import DBHelper
from kezbot import Config
from kezbot import dispatcher

owner_id = int(Config.OWNER_ID)  # Telegram user ID


@run_async
def chats(_bot, update):
    chat_id = str(update.effective_chat.id)
    chat_name = str(update.effective_chat.title)
    if len(chat_id) > 5:
        db.add_item(chat_id, chat_name)
    else:
        print('Could not add chat!')


@run_async
def get_chats(bot, update):
    chat_id = update.effective_chat.id
    get_items = db.get_items()
    count = get_items[2]
    bot.send_message(chat_id=chat_id,
                     text="I'm currently in {} groups".format(count),
                     parse_mode=telegram.ParseMode.HTML)


@run_async
def broadcast(bot, update):
    global failed
    sender = update.message.from_user
    if sender.id == owner_id:
        to_send = update.effective_message.text.split(None, 2)
        if len(to_send) <= 2:
            get_message = to_send[1]
            if len(get_message) >= 2:
                kez_chats = db.get_items()
                failed = 0
                for chat in kez_chats[0]:
                    chat_id = str(chat[0])
                    chat_name = str(chat[1])
                    try:
                        bot.sendMessage(int(chat_id), get_message)
                        sleep(0.1)
                    except TelegramError:
                        failed += 1
                        print("Couldn't send broadcast to {}, group name {}".format(chat_id, chat_name),
                              file=sys.stderr)
        else:
            chat_id = to_send[1]
            get_message = to_send[2]
            if len(get_message) >= 2:
                failed = 0
                try:
                    bot.sendMessage(int(chat_id), get_message)
                    sleep(0.1)
                except TelegramError:
                    failed += 1
                    print("Couldn't send broadcast to {}".format(chat_id),
                          file=sys.stderr)

            update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message, probably "
                                                "due to being kicked.".format(failed))
    else:
        update.message.reply_text("Sorry mate, can't do that.")


db = DBHelper()

BOT_STATS = CommandHandler("stats", get_chats)
BROADCAST = CommandHandler("broadcast", broadcast)
CHAT_HANDLER = MessageHandler(Filters.all & ~Filters.private, chats)

dispatcher.add_handler(BOT_STATS)
dispatcher.add_handler(BROADCAST)
dispatcher.add_handler(CHAT_HANDLER)
