from aiogram.filters import BaseFilter
from aiogram import types
import re



class CheckInstaLink(BaseFilter):
    async def __call__(self, message: types.Message):
        insta_regex = r"^https?:\/\/(www\.)?instagram\.com\/.*"
        return bool(re.match(insta_regex, message.text))
    


class YtCheckLink(BaseFilter):
    async def __call__(self, message: types.Message):
        youtube_regex = re.compile(
            r"(?:https?:\/\/)?(?:www\.)?" 
            r"(youtube\.com|youtu\.be)\/"  #
            r"(watch\?v=|embed\/|v\/|.+\?v=)?([^&\n]+)" 
        )

        return bool(youtube_regex.match(message.text))




class TiktokCheckLink(BaseFilter):
    async def __call__(self, message: types.Message):
        # TikTok URL'larining ikkalasini aniqlash uchun regex
        pattern = r"^(https:\/\/(www\.|vt\.)?tiktok\.com\/(@[\w\.]+\/video\/\d+|Z[\w]+\/))$"
        print("ss")
        # URL'ni topish uchun re.search ishlatamiz
        if re.search(pattern, message.text):
            print("s")
            return True
        return False