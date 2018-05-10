import spotipy
import spotipy.util as util
import telegram
from telegram.ext import run_async, CommandHandler

from kezbot import Config, dispatcher


@run_async
def search(_bot, update, args):
    if len(args) == 0:
        update.effective_message.reply_text("You forgot to give me a searchterm! \nTry again with: /playlist "
                                            "<your searchterm>")
    else:
        spotify_token = util.prompt_for_user_token(Config.USERNAME, Config.SCOPE)
        if spotify_token:
            text = ' '.join(args)
            spotify = spotipy.Spotify(auth=spotify_token)
            results = spotify.search(q="{}".format(text), limit=10, type="playlist")

            playlist = ''
            for item in results['playlists']['items']:
                playlist += '\n► <a href="{0}">{1}</a> | {2} tracks' \
                    .format(item['external_urls']['spotify'], item['name'], item['tracks']['total'])

            update.effective_message.reply_text("<b>Top 10 playlists matching:</b> {0}\n"
                                                "{1}".format(text, playlist),
                                                parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            print("There's something wrong with the token")


__mod_name__ = "playlists"

GET_PLAYLIST = CommandHandler("playlist", search, pass_args=True)
dispatcher.add_handler(GET_PLAYLIST)
