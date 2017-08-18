from telegram.ext import BaseFilter
import re


class __UrlFilter(BaseFilter):
    def filter(self, message):
        return 'watch?'in message.text

UrlFilter = __UrlFilter()
