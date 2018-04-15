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
    getText = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    ytUrl = ''.join(list([y if t.type == MessageEntity.URL
                          else t.url for t, y in getText.items()][0]))
    pattern = YTMatchPattern

    if re.match(pattern, ytUrl, re.I):
        ytLink = ytUrl
        pattern = YoutubePattern
        ytId = ' '.join(re.findall(pattern, ytLink, re.MULTILINE | re.IGNORECASE))

        if not ytId:
            update.effective_message.reply_text("This is not a valid Youtube-URL! \nTry again.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}" \
                .format(ytId, api)
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
                newList = list(filter(None, re.split(split, result)))

                first = newList[0]
                sep = 'aka'
                sep2 = 'AKA'
                newList[0] = first.split(sep, 1)[0]
                newList[0] = first.split(sep2, 1)[0]

                spotifyToken = util.prompt_for_user_token(Config.username, Config.scope)

                if spotifyToken:
                    spot = spotipy.Spotify(auth=spotifyToken)
                    artist = newList[0]
                    track = newList[1]

                    results = spot.search(q="artist:{} track:{}".format(artist, track, limit=1))

                    if results:
                        spotTracks = results['tracks']['items']
                        if spotTracks:
                            spotArtist = spotTracks[0]['artists'][0]['name']
                            spotTitle = spotTracks[0]['name']
                            spotUrl = spotTracks[0]['external_urls']['spotify']
                            update.effective_message.reply_text \
                                ("► {0} - {1} \n{2}".format(spotArtist, spotTitle, spotUrl))
                        else:
                            results = spot.search(q="artist:{} track:{}"
                                                  .format(track, artist, limit=1))
                            spotTracks = results['tracks']['items']
                            if spotTracks:
                                spotArtist = spotTracks[0]['artists'][0]['name']
                                spotTitle = spotTracks[0]['name']
                                spotUrl = spotTracks[0]['external_urls']['spotify']
                                update.effective_message.reply_text \
                                    ("► {0} - {1} \n{2}".format(spotArtist, spotTitle, spotUrl))
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
