#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from random import randint
from time import sleep
import requests
import urllib.error
import urllib.request
import simplejson
import spotipy
import spotipy.util as util
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from strings import YoutubePattern, MatchPattern, RemoveWords, StringRegex, run_strings

OWNER_ID = int(Config.OWNER_ID)  # Telegram user ID


@run_async
def getify(bot, update):
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
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}".format(yt_id, api)
            json = simplejson.load(urllib.request.urlopen(url))
            title = json['items'][0]['snippet']['title']  # get title from Youtube
            strips = [' - ', '- ', ' -', ': ', ' : ', ' :', ' – ']

            if not any(e in title for e in strips):
                update.effective_message.reply_text('This is not a valid song, try a different url')
            else:
                update.effective_message.reply_text("You've searched for: \n♫ {0}. \n\nLet me find it on Spotify!"
                                                    .format(title))
                result = re.compile(RemoveWords, re.I)
                result = result.sub("", title).strip()

                for m in re.finditer(r'\([^()]+\)', result):
                    if not re.search(r'\b(remix|edit|rmx)\b', m.group(), re.I):
                        result = re.sub(re.escape(m.group()), '', result)
                result = re.sub(StringRegex, '', result).strip()
                result = ' '.join(result.split())

                split = ' - |- | -|: | : | :| – '
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
                            spotitle = spottracks[0]['name']
                            spoturl = spottracks[0]['external_urls']['spotify']
                            update.effective_message.reply_text("► {0} - {1} \n{2}"
                                                                .format(spotartist, spotitle, spoturl))
                        else:
                            results = spot.search(q="artist:{} track:{}".format(track, artist, limit=1))
                            spottracks = results['tracks']['items']
                            if spottracks:
                                spotartist = spottracks[0]['artists'][0]['name']
                                spotitle = spottracks[0]['name']
                                spoturl = spottracks[0]['external_urls']['spotify']
                                update.effective_message.reply_text("► {0} - {1} \n{2}"
                                                                    .format(spotartist, spotitle, spoturl))
                            else:
                                update.effective_message.reply_text("I can't find this track on Spotify :( "
                                                "Try a different link or search for another song.")
                    else:
                        update.effective_message.reply_text("This is not a song. Try some music :)")
                else:
                    print("There's something wrong with the Spotify token")


@run_async
def start(bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm KezBot. Send me a Youtube-URL and I'll give you a Spotify-URL to that song!"
        .format(update.message.from_user.first_name))


@run_async
def runs(bot, update):
    sleep(3)
    start_running = randint(0, len(run_strings)-1)
    update.effective_message.reply_text(run_strings[start_running])


def get_id(bot, update):
    sender = update.message.from_user
    sender_id = str(sender.id)
    update.effective_message.reply_text("Your ID is " + sender_id)


def get_ip(bot, update):  # get bot ip
    sender = update.message.from_user
    if sender.id == 18673980:
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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
