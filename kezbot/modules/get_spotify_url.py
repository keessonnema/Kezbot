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
from kezbot.strings import yt_match_pattern, youtube_pattern, strips, split, remove_words, \
    keep_words, string_regex


@run_async
def get_sp_url(_bot, update):
    API = Config.YOUTUBE_API_KEY
    get_text = update.effective_message.parse_entities \
        (types=[MessageEntity.URL, MessageEntity.TEXT_LINK])
    youtube_url = ''.join(list([y if t.type == MessageEntity.URL
                                else t.url for t, y in get_text.items()][0]))

    if re.match(yt_match_pattern, youtube_url, re.I):
        youtube_id = ' '.join(re.findall(youtube_pattern, youtube_url, re.MULTILINE | re.IGNORECASE))

        if not youtube_id:
            update.effective_message.reply_text("This is not a valid Youtube-URL! \nTry again.")
        else:
            url = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id={0}&key={1}" \
                .format(youtube_id, API)
            load_url = ujson.loads(requests.get(url).text)
            song_title = load_url['items'][0]['snippet']['title']

            if not any(e in song_title for e in strips):
                if update.message.chat.type == "private":
                    update.effective_message.reply_text('This is not a valid song :('
                                                        '\nTry a different link or search for another song.')
            else:
                filter_title = re.compile(remove_words, re.I)
                result = filter_title.sub('', song_title).strip()

                for m in re.finditer(r'\([^()]+\)', result):
                    if not re.search(keep_words, m.group(), re.I):
                        result = re.sub(re.escape(m.group()), '', result)
                filter_strings = re.sub(string_regex, '', result).strip()
                result = ' '.join(filter_strings.split())
                new_list = list(filter(None, re.split(split, result)))

                first = new_list[0]
                sep = 'aka'
                sep2 = 'AKA'
                new_list[0] = first.split(sep, 1)[0]
                new_list[0] = first.split(sep2, 1)[0]

                spotify_token = util.prompt_for_user_token(Config.USERNAME, Config.SCOPE)

                if spotify_token:
                    spotify = spotipy.Spotify(auth=spotify_token)
                    artist = new_list[0]
                    track = new_list[1]
                    results = spotify.search(q="artist:{} track:{}".format(artist, track, limit=1))

                    if results:
                        spot_tracks = results['tracks']['items']

                        if spot_tracks:
                            spot_artist = spot_tracks[0]['artists'][0]['name']
                            spot_title = spot_tracks[0]['name']
                            spot_url = spot_tracks[0]['external_urls']['spotify']
                            update.effective_message.reply_text \
                                ("► {0} - {1} \n{2}".format(spot_artist, spot_title, spot_url))
                        else:
                            results = spotify.search(q="artist:{} track:{}".format(track, artist, limit=1))
                            spot_tracks = results['tracks']['items']

                            if spot_tracks:
                                spot_artist = spot_tracks[0]['artists'][0]['name']
                                spot_title = spot_tracks[0]['name']
                                spot_url = spot_tracks[0]['external_urls']['spotify']
                                update.effective_message.reply_text \
                                    ("► {0} - {1} \n{2}".format(spot_artist, spot_title, spot_url), disable_web_page_preview=True)
                            else:
                                if update.message.chat.type == "private":
                                    update.effective_message.reply_text \
                                        ("I can't find this track on Spotify :( "
                                         "\nTry a different link or search for another song.")
                else:
                    print("There's something wrong with the Spotify token")


__mod_name__ = "get_spotify"

FILTER_YT_URL = MessageHandler(Filters.text & Filters.entity(MessageEntity.URL), get_sp_url)
dispatcher.add_handler(FILTER_YT_URL, group=3)
