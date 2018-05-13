import telegram
from telegram.ext import run_async, CommandHandler, MessageHandler, Filters

from kezbot.database import DBHelper
from kezbot import Config
from kezbot import dispatcher

OWNER = int(Config.OWNER_ID)


@run_async
def chats(_bot, update):
    chat_id = str(update.effective_chat.id)
    chat_name = str(update.effective_chat.title)
    if len(chat_id) > 5:
        db.add_item(chat_id, chat_name)
    else:
        print('Could not add chat!')


@run_async
def get_chat_count(bot, update):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if user_id == OWNER:
        count = db.get_chat_count()
        bot.send_message(chat_id=chat_id,
                         text="I'm currently in {} groups".format(count),
                         parse_mode=telegram.ParseMode.HTML)


@run_async
def get_chat_names(bot, update):
    user_id = update.effective_user.id

    if user_id == OWNER:
        chat_id = update.effective_chat.id
        get_chats = db.get_chat_names()

        chat_names = ''
        for get_chat in get_chats:
            chat_names += '\n- {0}'.format(get_chat[0])

        bot.send_message(chat_id=chat_id,
                         text="<b>I'm in the following chats:</b> {0}\n".format(chat_names),
                         parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text("Sorry mate, only my owner can use this command.")


db = DBHelper()

__mod_name__ = "get_chats"

BOT_STATS = CommandHandler("stats", get_chat_count)
CHAT_NAMES = CommandHandler("chats", get_chat_names)
CHAT_HANDLER = MessageHandler(Filters.all & ~Filters.private, chats)

dispatcher.add_handler(BOT_STATS)
dispatcher.add_handler(CHAT_NAMES)
dispatcher.add_handler(CHAT_HANDLER, group=4)
