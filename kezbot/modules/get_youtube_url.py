import pprint
import re
import requests
import ujson
import spotipy
import spotipy.util as util
import telegram
from telegram.ext import MessageHandler, Filters, CommandHandler

from kezbot import dispatcher
from kezbot.config import Config
from telegram.ext.dispatcher import run_async
from telegram import MessageEntity
from kezbot.strings import SPMatchPattern, YoutubePattern, strips, split, RemoveWords, \
    KeepWords, StringRegex, SpotifyPattern


@run_async
def get_yt_url(_bot, update):
    get_text = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    sp_url = ''.join(list([y if t.type == MessageEntity.URL
                           else t.url for t, y in get_text.items()][0]))

    pattern = SPMatchPattern
    if re.match(pattern, sp_url, re.I):
        sp_link = sp_url

        pattern = SpotifyPattern
        sp_id = re.findall(pattern, sp_link, re.MULTILINE | re.IGNORECASE)

        if not sp_id:
            update.effective_message.reply_text("This is not a valid Spotify-URL! \nTry again.")
        else:
            spotify_token = util.prompt_for_user_token(Config.username, Config.scope)

            if spotify_token:
                spot = spotipy.Spotify(auth=spotify_token)
                track = spot.track(sp_id[0][0])

                artist = track['artists'][0]['name']
                track = track['name']
                track = re.sub('- ', '', track)
                title = ''.join(artist + ' - ' + track)
                key = Config.YOUTUBE_API_KEY
                url = ("https://www.googleapis.com/youtube/v3/search?part=snippet&q={0}&key={1}"
                             .format(str(title), key))
                video_info = ujson.loads(requests.get(url).text)
                video_id = re.sub("'", '', video_info['items'][0]['id']['videoId'])
                video_url = ("https://youtube.com/watch?v={0}".format(video_id))
                update.effective_message.reply_text \
                    ("► {0} - {1} \n{2}".format(artist, track, video_url))


__mod_name__ = "getYoutube"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_yt_url)
dispatcher.add_handler(FILTER_YT_URL, group=2)
