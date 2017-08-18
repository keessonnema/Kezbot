#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re
import urllib.error
import urllib.request
import requests
import simplejson
import spotipy
import spotipy.util as util
from config import Config
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from telegram.ext.dispatcher import run_async
from strings import YoutubePattern, MatchPattern, RemoveWords
from custom_filters import UrlFilter
import strings

OWNER_ID = int(Config.OWNER_ID)  # Telegram user ID


@run_async
def get_url(bot, update):
    api = Config.YOUTUBE_API_KEY  # Youtube API

    url = update.effective_message.text
    pattern = MatchPattern

    if re.match(pattern, url, re.I):
        get_link = update.effective_message
        yt_link = get_link['text']
        pattern = YoutubePattern
        video_id = ' '.join(re.findall(pattern, yt_link, re.MULTILINE | re.IGNORECASE))

        if not video_id:
            update.effective_message.reply_text("This is not a Youtube-url! \nTry again with a Youtube-url.")
            print("This is not a Youtube-url.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}".format(video_id, api)
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
                result = re.sub(r'\[[^\]]*\]|\(\d+\)|“.*?”|".*?"|[.]|[&]|[,]|(#[A-Za-z0-9]+)', '', result).strip()

                split = ' - |- | -|: | : | :| – '
                new_list = list(filter(None, re.split(split, result)))

                first = new_list[0]
                sep = 'aka'
                new_list[0] = first.split(sep, 1)[0]

                # Spotify credentials
                os.environ["SPOTIPY_CLIENT_ID"] = Config.SPOT_CLIENT_ID
                os.environ["SPOTIPY_CLIENT_SECRET"] = Config.SPOT_CLIENT_SECRET
                os.environ["SPOTIPY_REDIRECT_URI"] = Config.SPOT_REDIRECT_URI

                username = Config.SPOT_USERNAME
                scope = Config.SPOT_SCOPE
                token = util.prompt_for_user_token(username, scope)

                if token:
                    spot = spotipy.Spotify(auth=token)
                    artist = new_list[0]
                    track = new_list[1]

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
                                update.effective_message.reply_text("► {0} - {1} {2}"
                                                                    .format(spotartist, spotitle, spoturl))
                            else:
                                update.effective_message.reply_text("I can't find this track on Spotify :( "
                                                                    "Try a different link or search for another song.")
                    else:
                        update.effective_message.reply_text("This is not a song. Try some music :)")

                else:
                    print("There's something wrong with the token")


@run_async
def getify(bot, update, args):
    api = Config.YOUTUBE_API_KEY  # Youtube API
    if len(args) == 0:
        update.effective_message.reply_text("You forgot to give me a Youtube-url! \nTry again with: /getify "
                                            "<youtube-url>.")
    else:
        getify_link = args[0]
        pattern = YoutubePattern
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
            result = re.compile(RemoveWords, re.I)
            result = result.sub("", title).strip()
            result = re.sub(r'\[[^\]]*\]|\(\d+\)|“.*?”|[.]|[&]|[,]|(#[A-Za-z0-9]+)', '', result).strip()

            new_list = list(filter(None, re.split(' - |- | -|: | : | :| – ', result)))  # split on '- / : / –',
                                                                           # and ignore empty strings
            first = new_list[0]
            sep = 'aka'
            new_list[0] = first.split(sep, 1)[0]

            # Spotify credentials
            os.environ["SPOTIPY_CLIENT_ID"] = Config.SPOT_CLIENT_ID
            os.environ["SPOTIPY_CLIENT_SECRET"] = Config.SPOT_CLIENT_SECRET
            os.environ["SPOTIPY_REDIRECT_URI"] = Config.SPOT_REDIRECT_URI

            username = Config.SPOT_USERNAME
            scope = Config.SPOT_SCOPE
            token = util.prompt_for_user_token(username, scope)

            if token:
                spot = spotipy.Spotify(auth=token)
                artist = new_list[0]
                track = new_list[1]

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
@run_async
def start(bot, update):
    update.effective_message.reply_text(
        "Hello {}. I'm KezBot. Send me a Youtube-URL and I'll give you a Spotify-URL to that song!"
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

    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_url))
    #updater.dispatcher.add_handler(CommandHandler("getify", getify, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('hardtraxx', hardtraxx))
    updater.dispatcher.add_handler(CommandHandler("ip", get_ip))
    updater.dispatcher.add_handler(CommandHandler("id", get_id))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
