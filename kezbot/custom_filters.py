from telegram.ext import BaseFilter
import re


class __UrlFilter(BaseFilter):
    def filter(self, message):
        return message.entities and any(msg.type == 'url' for msg in message.entities)


UrlFilter = __UrlFilter()
