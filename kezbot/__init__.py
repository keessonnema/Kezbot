import logging
import os

import telegram.ext as tg
from kezbot.config import Config

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "translation").split()

TOKEN = Config.API_KEY
updater = tg.Updater(TOKEN)
dispatcher = updater.dispatcher
