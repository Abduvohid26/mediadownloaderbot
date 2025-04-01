from aiogram.filters import BaseFilter
from aiogram import types
import re


class CheckInstaLink(BaseFilter):
    async def __call__(self, message: types.Message):
        if message.text.startswith('https://instagram.com'):
            return True
        elif message.text.startswith('https://www.instagram.com'):
            return True

        elif message.text.startswith('http://instagram.com'):
            return True

        elif message.text.startswith('http://www.instagram.com'):
            return True
        else:
            return False


class YtCheckLink(BaseFilter):
    async def __call__(self, message: types.Message):
        youtube_regex = re.compile(
            r"(?:https?:\/\/)?(?:www\.)?"  # HTTP yoki HTTPS bo'lishi mumkin
            r"(youtube\.com|youtu\.be)\/"  # youtube.com yoki youtu.be domenlari
            r"(watch\?v=|embed\/|v\/|.+\?v=)?([^&\n]+)"  # video ID qismi
        )

        return bool(youtube_regex.match(message.text))
