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
from kezbot.strings import sp_match_pattern, spotify_pattern


@run_async
def get_yt_url(_bot, update):
    message = update.effective_message.parse_entities(types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    spotify_url = ''.join(list([y if t.type == MessageEntity.URL else t.url for t, y in message.items()][0]))

    if re.match(sp_match_pattern, spotify_url, re.I):
        spotify_id = re.findall(spotify_pattern, spotify_url, re.MULTILINE | re.IGNORECASE)
        if spotify_id:
            spotify_token = util.prompt_for_user_token(Config.USERNAME, Config.SCOPE)
            if spotify_token:
                spotify = spotipy.Spotify(auth=spotify_token)
                result = spotify.track(spotify_id[0][0])

                artist = result['artists'][0]['name']
                track = re.sub('- ', '', result['name'])
                title = ''.join(artist.replace('&', '') + ' - ' + track)

                youtube_key = Config.YOUTUBE_API_KEY
                youtube_url = ("https://www.googleapis.com/youtube/v3/search?part=snippet&q={0}&key={1}"
                               .format(str(title), youtube_key))
                video_info = ujson.loads(requests.get(youtube_url).text)

                if 'videoId' in video_info['items'][0]['id']:
                    get_video_id = re.sub("'", '', video_info['items'][0]['id']['videoId'])
                    video_url = ("https://youtube.com/watch?v={0}".format(get_video_id))
                    update.effective_message.reply_text \
                        ("► {0} - {1} \n{2}".format(artist, track, video_url), disable_web_page_preview=True)
                else:
                    print('No videoId!')
            else:
                print("There's something wrong with the token.")


__mod_name__ = "get_youtube"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_yt_url)
dispatcher.add_handler(FILTER_YT_URL, group=2)
