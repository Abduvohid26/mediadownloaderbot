from loader import dp, bot
from aiogram import types,F
import requests

from aiogram.enums.chat_action import ChatAction
from aiogram.types import  InputMediaPhoto, InputMediaVideo



@dp.message(F.text)

async def echo_bot(message:types.Message):
    url = message.text.strip()
    print(url, url[1:])
    new_url = f"https://www.instagram.com/stories/{url[1:]}/"
    info = await message.answer("Sorov Bajarilmoqda Kuting...")
    try:
        response = requests.post("http://95.169.205.213:8080/instagram/media", data={"url": new_url})
        data = response.json()
        print(data)
        if data["error"] == True:
                await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
                return
        elif data["type"] == "stories":
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO)

            photo_group = []
            video_group = []  

            for media in data["medias"]:
                if media["type"] == "video":
                    video_group.append(InputMediaVideo(media=media["download_url"], caption="Videos"))
                else:
                    photo_group.append(InputMediaPhoto(media=media["download_url"], caption="Photos"))

                if len(video_group) == 10:
                    await message.answer_media_group(video_group)
                    video_group = []

                if len(photo_group) == 10:
                    await message.answer_media_group(photo_group)
                    photo_group = []

            if video_group:
                await message.answer_media_group(video_group)

            if photo_group:
                await message.answer_media_group(photo_group)
    except Exception as e:
        print(e)
        await message.answer("Xatolik Yuz berdi Qayta urunib ko'ring")
    finally:
        await info.delete()



