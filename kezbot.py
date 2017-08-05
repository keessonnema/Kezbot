#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import configparser
import requests
import pprint
import strings
import os
import time
import sys
import logging
import spotipy
import spotipy.util as util
import urllib.request, urllib.error
import simplejson
import re
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config


def getify(bot, update, args):

    api = Config.YOUTUBE_API_KEY # Youtube API
    getify_link = args[0]
    pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
    result = ' '.join(re.findall(pattern, getify_link, re.MULTILINE | re.IGNORECASE))

    id = result
    url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}".format(id, api)
    json = simplejson.load(urllib.request.urlopen(url))

    # Extract and split from string to widen search.
    remb = r'\[[^\]]*\]'  # Remove square brackets + content from title
    title = json['items'][0]['snippet']['title']  # get title from Youtube
    pattern = re.compile("\\b(Official|Video|Mix|Music|ft.|HQ|version|HD|Original|12\")\\W", re.I) #Remove these words from the title
    result = pattern.sub("", title)
    result2 = re.sub(remb, '', result)
    result3 = re.sub(r'\(\d+\)', '', result2)
    update.effective_message.reply_text("You've searched for: \n{0}. \n\nLet me find it on Spotify!" .format(title))

    stripped = result3.split(" - ")
    newlist = list(filter(None, stripped))

    print(newlist)
    # Spotify credentials
    os.environ["SPOTIPY_CLIENT_ID"] = Config.SPOT_CLIENT_ID
    os.environ["SPOTIPY_CLIENT_SECRET"] = Config.SPOT_CLIENT_SECRET
    os.environ["SPOTIPY_REDIRECT_URI"] = Config.SPOT_REDIRECT_URI

    username = Config.SPOT_USERNAME
    scope = Config.SPOT_SCOPE
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        artist = newlist[0]
        track = newlist[1]

        results = sp.search(q="artist:{} track:{}".format(artist, track, limit=1))
#        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(results)

        if results:
            spotracks = results['tracks']['items']
            if spotracks:
                spotartist = spotracks[0]['artists'][0]['name']
                spotitle = spotracks[0]['name']
                spoturl = spotracks[0]['external_urls']['spotify']
                update.effective_message.reply_text("► {0} - {1} {2}".format(spotartist, spotitle, spoturl))
            else:
                update.effective_message.reply_text("I can't find this track on Spotify :( "
                                                    "Try a different link or search for another song.")
        else:
            update.effective_message.reply_text("This is not a song. Try some music :)")

    else:
        print("There's something wrong with the token")

# basic bot commands
owner_id = int(Config.OWNER_ID) # Telegram user ID


def start(bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm KezBot. Send me a Youtube-link "
        "(/getify <youtube-url>) and I'll give you a Spotify-URL to that song!".format(update.message.from_user.first_name))


def hello(bot, update):
    update.effective_message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def hardtraxx(bot, update):
    update.effective_message.reply_text("Hardstylboy was here!!!")


def ip(bot, update):
    sender = update.message.from_user

    if sender.id == owner_id:
        res = requests.get("http://ipinfo.io/ip")
        ip = res.text
        update.effective_message.reply_text("The server's IP is " + ip)
    else:
        update.effective_message.reply_text(strings.stringAdminOnly)


def getid(bot, update):
    sender = update.message.from_user

    sender_id = str(sender.id)

    update.effective_message.reply_text("Your ID is " + sender_id)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    token = Config.API_KEY
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler("getify", getify, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('hardtraxx', hardtraxx))
    updater.dispatcher.add_handler(CommandHandler("ip", ip))
    updater.dispatcher.add_handler(CommandHandler("id", getid))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
