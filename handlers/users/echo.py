from loader import dp, bot
from aiogram import types,F
import requests

from aiogram.enums.chat_action import ChatAction
from aiogram.types import  InputMediaPhoto, InputMediaVideo



# @dp.message(F.text)

# async def echo_bot(message:types.Message):
#     url = message.text.strip()
#     print(url, url[1:])
#     new_url = f"https://www.instagram.com/stories/{url[1:]}/"
#     info = await message.answer("Sorov Bajarilmoqda Kuting...")
#     try:
#         response = requests.post("http://95.169.205.213:8080/instagram/media", data={"url": new_url})
#         data = response.json()
#         print(data)
#         if data["error"] == True:
#                 await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
#                 return
#         elif data["type"] == "stories":
#             await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

#             photo_group = []
#             video_group = []  

#             for media in data["medias"]:
#                 if media["type"] == "video":
#                     video_group.append(InputMediaVideo(media=media["download_url"], caption="Videos"))
#                 else:
#                     photo_group.append(InputMediaPhoto(media=media["download_url"], caption="Photos"))

#                 if len(video_group) == 10:
#                     await message.answer_media_group(video_group)
#                     video_group = []

#                 if len(photo_group) == 10:
#                     await message.answer_media_group(photo_group)
#                     photo_group = []

#             if video_group:
#                 await message.answer_media_group(video_group)

#             if photo_group:
#                 await message.answer_media_group(photo_group)
#     except Exception as e:
#         print(e)
#         await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
#     finally:
#         await info.delete()

import httpx
from aiogram import Bot, types, F
from aiogram.types import InputMediaVideo, InputMediaPhoto
from aiogram.enums.chat_action import ChatAction
from loader import dp, bot
import asyncio

# @dp.message(F.text.contains("@"))
async def echo_bot(message: types.Message):
    url = message.text.strip()
    print(url, url[1:])
    new_url = f"https://www.instagram.com/stories/{url[1:]}/"
    info = await message.answer("Сoрoв Bajarilmoqda Kuting...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://videoyukla.uz/instagram/media", params={"in_url": new_url}, timeout=15)

            data = response.json()
        
        print(data)
        if data.get("error"):
            await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
            return

        if data["type"] == "image":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
            await message.answer_photo(data["medias"][0]["download_url"])

        elif data["type"] == "video":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
            await message.answer_video(data["medias"][0]["download_url"])

        elif data["type"]  == "album":
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