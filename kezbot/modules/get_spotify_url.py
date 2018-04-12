import re
import requests
import ujson
import spotipy
import spotipy.util as util
from telegram.ext import MessageHandler, Filters

from kezbot import dispatcher
from kezbot.config import Config
from telegram.ext.dispatcher import run_async
from telegram import MessageEntity
from kezbot.strings import YTMatchPattern, YoutubePattern, strips, split, RemoveWords, \
    KeepWords, StringRegex


@run_async
def get_sp_url(_bot, update):
    api = Config.YOUTUBE_API_KEY
    get_text = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    yt_url = ''.join(list([y if t.type == MessageEntity.URL
                           else t.url for t, y in get_text.items()][0]))
    pattern = YTMatchPattern

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


__mod_name__ = "getSpotify"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_sp_url)
dispatcher.add_handler(FILTER_YT_URL, group=3)
