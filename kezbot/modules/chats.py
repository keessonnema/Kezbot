from time import sleep

import sys
import telegram
from telegram import TelegramError
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters

from kezbot.database import DBHelper
from kezbot import Config
from kezbot import dispatcher

OWNER = int(Config.OWNER_ID)


@run_async
def chats(_bot, update):
    chatId = str(update.effective_chat.id)
    chatName = str(update.effective_chat.title)
    if len(chatId) > 5:
        db.add_item(chatId, chatName)
    else:
        print('Could not add chat!')


@run_async
def get_chats(bot, update):
    chatId = update.effective_chat.id
    getItems = db.get_items()
    count = getItems[2]
    bot.send_message(chat_id=chatId,
                     text="I'm currently in {} groups".format(count),
                     parse_mode=telegram.ParseMode.HTML)


@run_async
def broadcast(bot, update):
    global failed
    sender = update.message.from_user
    if sender.id == OWNER:
        toSend = update.effective_message.text.split(None, 2)
        if len(toSend) <= 2:
            get_message = toSend[1]
            if len(get_message) >= 2:
                kezChats = db.get_items()
                failed = 0
                for chat in kezChats[0]:
                    chatId = str(chat[0])
                    chatName = str(chat[1])
                    try:
                        bot.sendMessage(int(chatId), get_message)
                        sleep(0.1)
                    except TelegramError:
                        failed += 1
                        print("Couldn't send broadcast to {}, group name {}".format(chatId, chatName),
                              file=sys.stderr)
        else:
            chatId = toSend[1]
            getMessage = toSend[2]
            if len(getMessage) >= 2:
                failed = 0
                try:
                    bot.sendMessage(int(chatId), getMessage)
                    sleep(0.1)
                except TelegramError:
                    failed += 1
                    print("Couldn't send broadcast to {}".format(chatId),
                          file=sys.stderr)

            update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message, probably "
                                                "due to being kicked.".format(failed))
    else:
        update.message.reply_text("Sorry mate, can't do that.")


db = DBHelper()

__mod_name__ = "GetChats"

BOT_STATS = CommandHandler("stats", get_chats)
BROADCAST = CommandHandler("broadcast", broadcast)
CHAT_HANDLER = MessageHandler(Filters.all & ~Filters.private, chats)

dispatcher.add_handler(BOT_STATS)
dispatcher.add_handler(BROADCAST)
dispatcher.add_handler(CHAT_HANDLER, group=4)
