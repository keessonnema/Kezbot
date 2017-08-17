#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import urllib.error
import urllib.request
import pprint
import requests
import json as simplejson
import spotipy
import spotipy.util as util
from config import Config
from telegram.ext import Updater, CommandHandler

import strings

OWNER_ID = int(Config.OWNER_ID)  # Telegram user ID


def getify(bot, update, args):
    api = Config.YOUTUBE_API_KEY  # Youtube API
    if len(args) == 0:
        update.effective_message.reply_text("You forgot to give me a Youtube-url! \nTry again with: /getify "
                                            "<youtube-url>.")
        print("args are empty.")
    else:
        getify_link = args[0]
        pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
        video_id = ' '.join(re.findall(pattern, getify_link, re.MULTILINE | re.IGNORECASE))
        if not video_id:
            update.effective_message.reply_text("This is not a Youtube-url! \nTry again with: /getify <youtube-url>.")
            print("This is not a Youtube-url.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}".format(video_id, api)
            json = simplejson.load(urllib.request.urlopen(url))

            # Extract and split from string to widen search.
            title = json['items'][0]['snippet']['title']  # get title from Youtube
            update.effective_message.reply_text("You've searched for: \n♫ {0}. \n\nLet me find it on Spotify!"
                                                .format(title))
            # Remove words, square brackets, dots, other characters
            result = re.compile("\\b(Official|Video|Videoclip|Mix|Music|ft|feat|HQ|version|HD|Original"
                                "|Extended|Meets|12\"|lyrics|Lyrics|International)\\W", re.I)
            result = result.sub("", title)
            result = re.sub(r'\[[^\]]*\]', '', result)
            result = re.sub(r'[.]', ' ', result)
            result = re.sub(r'\(\d+\)', '', result)
            result = re.sub(r'“.*?”', '', result)
            result = re.sub(r'&', '', result)

            newlist = list(filter(None, result.split(' - ')))  # split on '-', and ignore empty strings

            # Spotify credentials
            os.environ["SPOTIPY_CLIENT_ID"] = Config.SPOT_CLIENT_ID
            os.environ["SPOTIPY_CLIENT_SECRET"] = Config.SPOT_CLIENT_SECRET
            os.environ["SPOTIPY_REDIRECT_URI"] = Config.SPOT_REDIRECT_URI

            username = Config.SPOT_USERNAME
            scope = Config.SPOT_SCOPE
            token = util.prompt_for_user_token(username, scope)

            if token:
                spot = spotipy.Spotify(auth=token)
                artist = newlist[0]
                track = newlist[1]

                results = spot.search(q="artist:{} track:{}".format(artist, track, limit=1))

                if results:
                    spottracks = results['tracks']['items']
                    if spottracks:
                        spotartist = spottracks[0]['artists'][0]['name']
                        spotitle = spottracks[0]['name']
                        spoturl = spottracks[0]['external_urls']['spotify']
                        update.effective_message.reply_text("► {0} - {1} {2}".format(spotartist, spotitle, spoturl))
                    else:
                        results = spot.search(q="artist:{} track:{}".format(track, artist, limit=1))
                        spottracks = results['tracks']['items']
                        if spottracks:
                            spotartist = spottracks[0]['artists'][0]['name']
                            spotitle = spottracks[0]['name']
                            spoturl = spottracks[0]['external_urls']['spotify']
                            update.effective_message.reply_text("► {0} - {1} {2}".format(spotartist, spotitle, spoturl))
                        else:
                            update.effective_message.reply_text("I can't find this track on Spotify :( "
                                                            "Try a different link or search for another song.")
                else:
                    update.effective_message.reply_text("This is not a song. Try some music :)")

            else:
                print("There's something wrong with the token")


# basic bot commands
def start(bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm KezBot. Send me a Youtube-link "
        "(/getify <youtube-url>) and I'll give you a Spotify-URL to that song!"
            .format(update.message.from_user.first_name))


def hello(bot, update):
    update.effective_message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def hardtraxx(bot, update):
    update.effective_message.reply_text("Hardstylboy was here!!!")


def get_ip(bot, update):
    sender = update.message.from_user

    if sender.id == OWNER_ID:
        res = requests.get("http://ipinfo.io/ip")
        ip_addr = res.text
        update.effective_message.reply_text("The server's IP is " + ip_addr)
    else:
        update.effective_message.reply_text(strings.stringAdminOnly)


def get_id(bot, update):
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
    updater.dispatcher.add_handler(CommandHandler("ip", get_ip))
    updater.dispatcher.add_handler(CommandHandler("id", get_id))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
