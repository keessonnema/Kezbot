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
    getMessage = update.effective_message.parse_entities(types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    spotifyUrl = ''.join(list([y if t.type == MessageEntity.URL else t.url for t, y in getMessage.items()][0]))

    if re.match(SPMatchPattern, spotifyUrl, re.I):
        spotifyId = re.findall(SpotifyPattern, spotifyUrl, re.MULTILINE | re.IGNORECASE)

        if not spotifyId:
            update.effective_message.reply_text("This is not a valid Spotify-URL! \nTry again.")
        else:
            spotifyToken = util.prompt_for_user_token(Config.username, Config.scope)
            if spotifyToken:
                spot = spotipy.Spotify(auth=spotifyToken)
                getSong = spot.track(spotifyId[0][0])

                artist = getSong['artists'][0]['name']
                track = re.sub('- ', '', getSong['name'])
                title = ''.join(artist + ' - ' + track)

                API = Config.YOUTUBE_API_KEY
                url = ("https://www.googleapis.com/youtube/v3/search?part=snippet&q={0}&key={1}"
                       .format(str(title), API))

                videoInfo = ujson.loads(requests.get(url).text)
                if 'videoId' in videoInfo['items'][0]['id']:
                    getVideoId = re.sub("'", '', videoInfo['items'][0]['id']['videoId'])
                    videoUrl = ("https://youtube.com/watch?v={0}".format(getVideoId))
                    videoTitle = re.sub("'", '', videoInfo['items'][0]['snippet']['title'])
                    update.effective_message.reply_text("► {0} \n{1}".format(videoTitle, videoUrl))
                else:
                    print('No videoId!')


__mod_name__ = "getYoutube"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_yt_url)
dispatcher.add_handler(FILTER_YT_URL, group=2)
