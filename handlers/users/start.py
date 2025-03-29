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
    print(data)
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
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            media_group = []
            for media in data["medias"]:
                if media["type"] == "video":
                    media_group.append(InputMediaVideo(media=media["download_url"]))  # media= deb ko'rsatish shart
                else:
                    media_group.append(InputMediaPhoto(media=media["download_url"]))  # media= deb ko'rsatish shart

            await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            await message.answer_media_group(media_group)
        elif data["type"] == "stories":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

            photo_group = []  # Rasmlar uchun
            video_group = []  # Videolar uchun

            for media in data["medias"]:
                if media["type"] == "video":
                    video_group.append(InputMediaVideo(media=media["download_url"]))
                else:
                    photo_group.append(InputMediaPhoto(media=media["download_url"]))

                # Agar videolar 10 taga yetsa, jo‘natib tashlaymiz
                if len(video_group) == 10:
                    await message.answer_media_group(video_group)
                    video_group = []

                # Agar rasmlar 10 taga yetsa, jo‘natib tashlaymiz
                if len(photo_group) == 10:
                    await message.answer_media_group(photo_group)
                    photo_group = []

            # Qolgan videolarni jo‘natish
            if video_group:
                await message.answer_media_group(video_group)

            # Qolgan rasmlarni jo‘natish
            if photo_group:
                await message.answer_media_group(photo_group)
    except Exception as e:
        print("error", e)
        await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
    finally:
        await info.delete()
