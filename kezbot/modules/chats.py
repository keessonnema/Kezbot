import telegram
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
    countItems = getItems[2]
    bot.send_message(chat_id=chatId, text="I'm currently in {} groups".format(countItems),
                     parse_mode=telegram.ParseMode.HTML)


db = DBHelper()

__mod_name__ = "GetChats"

BOT_STATS = CommandHandler("stats", get_chats)
CHAT_HANDLER = MessageHandler(Filters.all & ~Filters.private, chats)

dispatcher.add_handler(BOT_STATS)
dispatcher.add_handler(CHAT_HANDLER, group=4)
