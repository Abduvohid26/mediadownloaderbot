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
import asyncio

@dp.message(F.text, CheckInstaLink())
async def get_content(message: types.Message):
    url = message.text.strip()
    info = await message.answer("Sorov Bajarilmoqda Kuting...")

    max_retries = 3  # Maksimal urinishlar soni
    attempt = 0  # Joriy urinish soni

    while attempt < max_retries:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://videoyukla.uz/instagram/media", params={"in_url": url}, timeout=15)

                if response.status_code == 429:  
                    retry_after = int(response.headers.get("Retry-After", 1))  
                    print(f"Flood limit! Sleeping for {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                    attempt += 1
                    continue

                data = response.json()
            print(data, "Data")

            if data.get("error"):
                await message.answer("Xatolik Yuz berdi. Qayta urunib ko'ring!")
                return

            if data["type"] == "image":
                await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_PHOTO)
                await message.answer_photo(data["medias"][0]["download_url"])

            elif data["type"] == "video":
                await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)
                await message.answer_video(data["medias"][0]["download_url"])

            elif data["type"] == "album":
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
                        await asyncio.sleep(0.5) 

                if media_group:
                    await message.answer_media_group(media_group)

            break  # Agar muvaffaqiyatli bo‘lsa, siklni to‘xtatamiz

        except Exception as e:
            print("Error:", e)
            attempt += 1
            await asyncio.sleep(1)  # Har qanday xatodan keyin biroz kutish

    if attempt == max_retries:
        await message.answer("Juda ko'p urinish, iltimos, biroz kuting.")

    await info.delete()



from aiogram.filters import Command

@dp.message(Command("check"))
async def check(message: types.Message):
    
    await message.answer_video(video=f"")