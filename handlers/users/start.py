from aiogram.filters import CommandStart
from loader import dp, bot
from aiogram import types, F
import requests
from filters.my_filter import CheckInstaLink
from aiogram.enums.chat_action import ChatAction




@dp.message(CommandStart())
async def start_bot(message:types.Message):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}! Insatgram Link Yuboring")

from aiogram.types import  InputMediaPhoto, InputMediaVideo

@dp.message(F.text, CheckInstaLink())
async def get_content(message:types.Message):
    url = message.text.strip()
    info = await message.answer("Sorov Bajarilmoqda Kuting...")
    response = requests.post("http://95.169.205.213:8080/instagram/media", data={"url": url})
    data = response.json()
    print(data, 'data')
    if data["type"] == "album":
        print("album")
    try:
        if data["error"] == True:
            await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring1")
            return
        if data["type"] == "image":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await message.answer_photo(data["medias"][0]["download_url"])
        elif data["type"] == "video":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            await message.answer_video(data["download_url"])
        elif data["type"] == "album":
            print("salom")
            media_group = []
            for media in data["medias"]:
                if media["type"] == "video":
                    media_group.append(InputMediaVideo(media=media["download_url"]))  # media= deb ko'rsatish shart
                else:
                    media_group.append(InputMediaPhoto(media=media["download_url"]))  # media= deb ko'rsatish shart

            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            await message.answer_media_group(media_group)
        elif data["type"] == "stories":
            media_group = []
            for media in data["medias"]:
                if media["type"] == "video":
                    media_group.append(InputMediaVideo(media=media["download_url"]))
                else:
                    media_group.append(InputMediaPhoto(media=media["download_url"]))
            await bot.send_chat_action(chat_id=message.chat.id, action="upload_video")
            await message.answer_media_group(media_group)
    except Exception as e:
        print(e)
        await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
    finally:
        await info.delete()
