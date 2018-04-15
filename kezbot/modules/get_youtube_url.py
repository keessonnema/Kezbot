import re
import requests
import ujson
import spotipy
import spotipy.util as util

from telegram.ext import MessageHandler, Filters
from telegram import MessageEntity
from telegram.ext.dispatcher import run_async

from kezbot import dispatcher
from kezbot.config import Config
from kezbot.strings import SPMatchPattern, SpotifyPattern


@run_async
def get_yt_url(_bot, update):
    getText = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    spUrl = ''.join(list([y if t.type == MessageEntity.URL
                          else t.url for t, y in getText.items()][0]))

    pattern = SPMatchPattern
    if re.match(pattern, spUrl, re.I):
        pattern = SpotifyPattern
        spId = re.findall(pattern, spUrl, re.MULTILINE | re.IGNORECASE)

        if not spId:
            update.effective_message.reply_text("This is not a valid Spotify-URL! \nTry again.")
        else:
            spotifyToken = util.prompt_for_user_token(Config.username, Config.scope)
            if spotifyToken:
                spot = spotipy.Spotify(auth=spotifyToken)
                track = spot.track(spId[0][0])

                artist = track['artists'][0]['name']
                track = track['name']
                track = re.sub('- ', '', track)
                title = ''.join(artist + ' - ' + track)

                key = Config.YOUTUBE_API_KEY
                url = ("https://www.googleapis.com/youtube/v3/search?part=snippet&q={0}&key={1}"
                       .format(str(title), key))

                videoInfo = ujson.loads(requests.get(url).text)
                if 'videoId' in videoInfo['items'][0]['id']:
                    getVideoId = re.sub("'", '', videoInfo['items'][0]['id']['videoId'])
                    videoUrl = ("https://youtube.com/watch?v={0}".format(getVideoId))
                    update.effective_message.reply_text \
                        ("► {0} - {1} \n{2}".format(artist, track, videoUrl))
                else:
                    print('No videoId!')


__mod_name__ = "getYoutube"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_yt_url)
dispatcher.add_handler(FILTER_YT_URL, group=2)
