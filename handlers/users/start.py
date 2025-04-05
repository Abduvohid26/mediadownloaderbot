from aiogram.filters import CommandStart
from loader import dp, bot
from aiogram import types, F
import requests
from filters.my_filter import CheckInstaLink, YtCheckLink
from aiogram.enums.chat_action import ChatAction




@dp.message(CommandStart())
async def start_bot(message:types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}! Insatgram Link Yuboring")

from aiogram.types import  InputMediaPhoto, InputMediaVideo

import httpx

@dp.message(F.text, CheckInstaLink())
async def get_content(message: types.Message):
    url = message.text.strip()
    info = await message.answer("Sorov Bajarilmoqda Kuting...")

    async with httpx.AsyncClient() as client:
        response = await client.post("https://videoyukla.uz/instagram/media", data={"url": url}, timeout=15)
        data = response.json()


    try:
        if data.get("error"):
            await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring!")
            return

        if data["type"] == "image":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await message.answer_photo(data["medias"][0]["download_url"])

        elif data["type"] == "video":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            await message.answer_video(data["download_url"])

        elif data["type"] in ["album", "stories"]:
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

            media_group = []
            for media in data["medias"]:
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




from aiogram.filters import Command

@dp.message(Command("check"))
async def check(message: types.Message):
    
    await message.answer_video(video=f"")