#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from random import randint
from time import sleep
import requests
import ujson
import spotipy
import spotipy.util as util
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from strings import MatchPattern, YoutubePattern, strips, split, RemoveWords, \
    KeepWords, StringRegex, run_strings

OWNER_ID = int(Config.OWNER_ID)  # Telegram user ID


@run_async
def getify(_bot, update):
    api = Config.YOUTUBE_API_KEY  # Youtube API
    yt_url = update.effective_message.text
    pattern = MatchPattern

    if re.match(pattern, yt_url, re.I):
        yt_link = yt_url
        pattern = YoutubePattern
        yt_id = ' '.join(re.findall(pattern, yt_link, re.MULTILINE | re.IGNORECASE))

        if not yt_id:
            update.effective_message.reply_text("This is not a Youtube-URL! \nTry again.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}"\
                .format(yt_id, api)
            title = ujson.loads(requests.get(url).text)
            title = title['items'][0]['snippet']['title']  # get title from Youtube

            if not any(e in title for e in strips):
                update.effective_message.reply_text('This is not a valid song, try a different url')
            else:
                update.effective_message.reply_text("You've searched for: \n♫ {0}. \n\n"
                                                    "Let me find it on Spotify!".format(title))
                result = re.compile(RemoveWords, re.I)
                result = result.sub("", title).strip()

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

                print(new_list)

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
                            update.effective_message.reply_text\
                                ("► {0} - {1} \n{2}".format(spotartist, spottitle, spoturl))
                        else:
                            results = spot.search(q="artist:{} track:{}"
                                                  .format(track, artist, limit=1))
                            spottracks = results['tracks']['items']
                            if spottracks:
                                spotartist = spottracks[0]['artists'][0]['name']
                                spottitle = spottracks[0]['name']
                                spoturl = spottracks[0]['external_urls']['spotify']
                                update.effective_message.reply_text\
                                    ("► {0} - {1} \n{2}".format(spotartist, spottitle, spoturl))
                            else:
                                update.effective_message.reply_text\
                                    ("I can't find this track on Spotify :( "
                                     "Try a different link or search for another song.")
                    else:
                        update.effective_message.reply_text("This is not a song. Try some music :)")
                else:
                    print("There's something wrong with the Spotify token")


@run_async
def start(_bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm KezBot. Send me a Youtube-URL and I'll give you a Spotify-URL to that song!"
        .format(update.message.from_user.first_name))


@run_async
def runs(_bot, update):
    sleep(3)
    start_running = randint(0, len(run_strings)-1)
    update.effective_message.reply_text(run_strings[start_running])


@run_async
def get_id(_bot, update):
    sender = update.message.from_user
    sender_id = str(sender.id)
    update.effective_message.reply_text("Your ID is " + sender_id)


@run_async
def get_ip(_bot, update):
    sender = update.message.from_user
    if sender.id == Config.OWNER_ID:
        ip = requests.get("http://ipinfo.io/ip")
        update.message.reply_text(ip.text)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    token = Config.API_KEY
    updater = Updater(token)
    handler = updater.dispatcher.add_handler

    handler(MessageHandler(Filters.text, getify))
    handler(CommandHandler('start', start))
    handler(CommandHandler('runs', runs))
    handler(CommandHandler("id", get_id))
    handler(CommandHandler("ip", get_ip))

    if Config.use_webhooks:
        cert_pem = Config.cert_pem
        webhook_url = Config.webhook_url

        updater.start_webhook(listen='127.0.0.1', port=5000, url_path=token)
        updater.bot.set_webhook(url=webhook_url + token,
                                certificate=open(cert_pem, 'rb'))
    else:
        updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
