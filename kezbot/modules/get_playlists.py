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
        spot = util.prompt_for_user_token(Config.username, Config.scope)
        if spot:
            text = ' '.join(args)
            spot = spotipy.Spotify(auth=spot)
            results = spot.search(q="{}".format(text), limit=10, type="playlist")

            playlist = ''
            for item in results['playlists']['items']:
                playlist += '\n► <a href="{0}">{1}</a> | {2} tracks' \
                    .format(item['external_urls']['spotify'], item['name'], item['tracks']['total'])

            update.effective_message.reply_text("<b>Top 10 playlists matching:</b> {0}\n"
                                                "{1}".format(text, playlist),
                                                parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True)
        else:
            print("There's something wrong with the Spotify token")


__mod_name__ = "Playlists"

GET_PLAYLIST = CommandHandler("playlist", search, pass_args=True)
dispatcher.add_handler(GET_PLAYLIST)
