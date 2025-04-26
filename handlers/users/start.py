from aiogram.filters import CommandStart, Command
from loader import dp, bot
from aiogram import types, F
import requests
from filters.my_filter import CheckInstaLink, YtCheckLink
from aiogram.enums.chat_action import ChatAction



@dp.message(Command('check'))
async def checker(msg: types.Message):
    await msg.answer_video(video=f"https://scontent-ams4-1.cdninstagram.com/o1/v/t16/f2/m86/AQNmd_I1bEai3xqI2JYRTtuYehu1v91snJUFYgpgA8_uiMkQPzVnaXuCAw7_agYIjuRRTQ-otYy_cr7wdwcQu4q7fGHpTnE2d38aCs0.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=110&vs=629398873249627_3863327341&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC9GRTQ3RTIxNEFDQ0Q3Njk1NjMzNkRDRDI5RjMxNEU5OF92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dLdWk2UnlpNkhkT0F0WUJBSFFTV2xRV2hLRjJicV9FQUFBRhUCAsgBACgAGAAbABUAACbk%2BNXt%2FZKWQBUCKAJDMywXQEM7peNT988YEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%3D%3D&_nc_rid=d6c7c77a56&ccb=9-4&oh=00_AfHOHm0Bk_u9vv3oQ4e9qhUej9LmU5waKOSq1T0oKE2uuA&oe=680EC71A&_nc_sid=d885a2")

@dp.message(CommandStart())
async def start_bot(message:types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}! Insatgram Link Yuboring")

from aiogram.types import  InputMediaPhoto, InputMediaVideo

import httpx

@dp.message(F.text, CheckInstaLink())
async def get_content(message: types.Message):
    url = message.text.strip()
    info = await message.answer("Sorov Bajarilmoqda Kuting...")

    async with httpx.AsyncClient(timeout=80) as client:
        response = await client.get("https://videoyukla.uz/instagram/media", params={"in_url": url}, timeout=15)
        data = response.json()
    try:
        if data.get("error"):
            await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring!")
            print("Error server")
            return

        if data["type"] == "image":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await message.answer_photo(data["medias"][0]["download_url"])

        elif data["type"] == "video":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            await message.answer_video(data["medias"][0]["download_url"])

        elif data["type"] in ["album", "stories"]:
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

            media_group = []
            for media in data["medias"]:
                print(media, "MEDIA")
                if media["type"] == "video":
                    media_group.append(InputMediaVideo(media=media["download_url"]))
                else:
                    media_group.append(InputMediaPhoto(media=media["download_url"]))

                if len(media_group) == 10:
                    await message.answer_media_group(media_group)
                    media_group = []

            if media_group:
                await message.answer_media_group(media_group)

    except Exception as e:
        print("Error:", e)
        await message.answer("Xatolik yuz berdi, qayta urunib ko'ring.")
    finally:
        await info.delete()



# from aiogram.types import InputFile

from aiogram.filters import Command
@dp.message(Command('check'))
async def check(msg: types.Message):
    await msg.answer_audio(audio=types.FSInputFile(path="media/audio_1744802181.mp3"))