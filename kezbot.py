#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pprint
import re
from random import randint
from time import sleep

import requests
import ujson
import spotipy
import spotipy.util as util
import sys
import telegram

from database import DBHelper
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import MessageEntity, ParseMode, bot, TelegramError
from strings import MatchPattern, YoutubePattern, strips, split, RemoveWords, \
    KeepWords, StringRegex, run_strings

owner_id = int(Config.OWNER_ID)  # Telegram user ID


@run_async
def getify(_bot, update):
    api = Config.YOUTUBE_API_KEY
    get_text = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    yt_url = ''.join(list([y if t.type == MessageEntity.URL
                           else t.url for t, y in get_text.items()][0]))
    pattern = MatchPattern

    if re.match(pattern, yt_url, re.I):
        yt_link = yt_url
        pattern = YoutubePattern
        yt_id = ' '.join(re.findall(pattern, yt_link, re.MULTILINE | re.IGNORECASE))

        if not yt_id:
            update.effective_message.reply_text("This is not a valid Youtube-URL! \nTry again.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}" \
                .format(yt_id, api)
            title = ujson.loads(requests.get(url).text)
            title = title['items'][0]['snippet']['title']  # get title from Youtube

            if not any(e in title for e in strips):
                if update.message.chat.type == "private":
                    update.effective_message.reply_text('This is not a valid song :('
                                                        '\nTry a different link or search for another song.')
            else:
                result = re.compile(RemoveWords, re.I)
                result = result.sub('', title).strip()

                for m in re.finditer(r'\([^()]+\)', result):
                    if not re.search(KeepWords, m.group(), re.I):
                        result = re.sub(re.escape(m.group()), '', result)
                result = re.sub(StringRegex, '', result).strip()
                result = ' '.join(result.split())
                new_list = list(filter(None, re.split(split, result)))

                first = new_list[0]
                sep = 'aka'
                sep2 = 'AKA'
                new_list[0] = first.split(sep, 1)[0]
                new_list[0] = first.split(sep2, 1)[0]

                spotify_token = util.prompt_for_user_token(Config.username, Config.scope)

                if spotify_token:
                    spot = spotipy.Spotify(auth=spotify_token)
                    artist = new_list[0]
                    track = new_list[1]

                    results = spot.search(q="artist:{} track:{}".format(artist, track, limit=1))

                    if results:
                        spottracks = results['tracks']['items']
                        if spottracks:
                            spotartist = spottracks[0]['artists'][0]['name']
                            spottitle = spottracks[0]['name']
                            spoturl = spottracks[0]['external_urls']['spotify']
                            update.effective_message.reply_text \
                                ("► {0} - {1} \n{2}".format(spotartist, spottitle, spoturl))
                        else:
                            results = spot.search(q="artist:{} track:{}"
                                                  .format(track, artist, limit=1))
                            spottracks = results['tracks']['items']
                            if spottracks:
                                spotartist = spottracks[0]['artists'][0]['name']
                                spottitle = spottracks[0]['name']
                                spoturl = spottracks[0]['external_urls']['spotify']
                                update.effective_message.reply_text \
                                    ("► {0} - {1} \n{2}".format(spotartist, spottitle, spoturl))
                            else:
                                if update.message.chat.type == "private":
                                    update.effective_message.reply_text \
                                        ("I can't find this track on Spotify :( "
                                         "\nTry a different link or search for another song.")
                else:
                    print("There's something wrong with the Spotify token")


def search(bot, update, args):
    chat_id = update.effective_chat.id
    if len(args) == 0:
        update.effective_message.reply_text("You forgot to give me a searchterm! \nTry again with: /sp "
                                            "<your searchterm>")
    else:
        sp = util.prompt_for_user_token(Config.username, Config.scope)
        if sp:
            text = ' '.join(args)
            spot = spotipy.Spotify(auth=sp)
            results = spot.search(q="{}".format(text), limit=10, type="playlist")

            playlist = ""
            for item in results['playlists']['items']:
                playlist += '\n► <a href="{0}">{1}</a> | {2} tracks' \
                    .format(item['external_urls']['spotify'], item['name'], item['tracks']['total'])

            update.effective_message.reply_text("<b>Top 10 playlists matching:</b> {0}\n"
                                                "{1}".format(text, playlist),
                                                parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            print("There's something wrong with the Spotify token")


@run_async
def start(_bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm Shifty. Send me a Youtube-URL and I'll give you a Spotify-URL to that song!"
            .format(update.message.from_user.first_name))


@run_async
def runs(_bot, update):
    start_running = randint(0, len(run_strings) - 1)
    update.effective_message.reply_text(run_strings[start_running])


@run_async
def get_id(_bot, update):
    sender = update.message.from_user
    sender_id = str(sender.id)
    update.effective_message.reply_text("Your ID is " + sender_id)


@run_async
def get_ip(_bot, update):
    sender = update.message.from_user
    if sender.id == owner_id:
        ip = requests.get("http://ipinfo.io/ip")
        update.message.reply_text(ip.text)
    else:
        update.message.reply_text("Sorry mate, can't do that.")


@run_async
def chats(_bot, update):
    chat_id = str(update.effective_chat.id)
    chat_name = str(update.effective_chat.title)
    print(chat_id, chat_name)
    if len(chat_id) > 5:
        db.add_item(chat_id, chat_name)
    else:
        print('Could not add chat!')


@run_async
def get_chats(bot, update):
    chat_id = update.effective_chat.id
    get = db.get_items()
    count = get[2]
    bot.send_message(chat_id=chat_id,
                     text="I'm currently in {} groups".format(count),
                     parse_mode=telegram.ParseMode.HTML)


@run_async
def broadcast(bot, update):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        chats = db.get_items()
        failed = 0
        for chat in chats[0]:
            chat_id = str(chat[0])
            chat_name = str(chat[1])
            try:
                bot.sendMessage(int(chat_id), to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                print("Couldn't send broadcast to {}, group name {}".format(chat_id, chat_name),
                      file=sys.stderr)

        update.effective_message.reply_text("Broadcast complete. {} groups failed to receive the message, probably "
                                            "due to being kicked.".format(failed))


db = DBHelper()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.WARNING)
    token = Config.API_KEY
    updater = Updater(token)
    handler = updater.dispatcher.add_handler

    handler(MessageHandler(Filters.text &
                           Filters.entity(MessageEntity.URL), getify))
    handler(CommandHandler('start', start))
    handler(CommandHandler('runs', runs))
    handler(CommandHandler("id", get_id))
    handler(CommandHandler("ip", get_ip))
    handler(CommandHandler("stats", get_chats))
    handler(CommandHandler("playlist", search, pass_args=True))
    handler(CommandHandler("broadcast", broadcast))

    chat_handler = MessageHandler(Filters.all & ~Filters.private, chats)
    updater.dispatcher.add_handler(chat_handler)

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
