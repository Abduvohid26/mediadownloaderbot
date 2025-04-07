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

@dp.message(F.text)
async def echo_bot(message: types.Message, bot):
    url = message.text.strip()
    print(url, url[1:])
    new_url = f"https://www.instagram.com/stories/{url[1:]}/"
    info = await message.answer("Сoрoв Bajarilmoqda Kuting...")

    max_retries = 3  # Maksimal urinishlar soni
    attempt = 0  # Joriy urinish soni

    while attempt < max_retries:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://videoyukla.uz/instagram/media", params={"in_url": new_url}, timeout=15)

                if response.status_code == 429:  # Too Many Requests xatosi
                    retry_after = int(response.headers.get("Retry-After", 1))  # Agar header bo‘lmasa, 3 soniya kutamiz
                    print(f"Flood limit! Sleeping for {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                    attempt += 1
                    continue

                data = response.json()

            print(data)
            if data.get("error"):
                await message.answer("Xatolik yuz berdi. Qayta urunib ko'ring.")
                return

            if data["type"] == "image":
                await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
                await message.answer_photo(data["medias"][0]["download_url"])

            elif data["type"] == "video":
                await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
                await message.answer_video(data["medias"][0]["download_url"])

            elif data["type"] == "album":
                await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)

                media_group = []
                for media in data["medias"]:
                    if media["type"] == "video":
                        media_group.append(InputMediaVideo(media=media["download_url"]))
                    else:
                        media_group.append(InputMediaPhoto(media=media["download_url"]))

                    if len(media_group) == 10:
                        await message.answer_media_group(media_group)
                        media_group = []
                        await asyncio.sleep(0.5)  # Oraliq kutish

                if media_group:
                    await message.answer_media_group(media_group)

            break  # Agar muvaffaqiyatli bo‘lsa, siklni to‘xtatamiz

        except httpx.HTTPStatusError as e:
            print(f"HTTP xato: {e}")
            attempt += 1
            await asyncio.sleep(1)

        except Exception as e:
            print("Error:", e)
            attempt += 1
            await asyncio.sleep(1)

    if attempt == max_retries:
        await message.answer("Juda ko'p urinish, iltimos, biroz kuting.")

    await info.delete()