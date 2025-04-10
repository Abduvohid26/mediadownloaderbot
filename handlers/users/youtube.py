from aiogram.filters import Command
from aiogram.types import FSInputFile
from loader import bot, dp
from aiogram import types
from aiogram.enums.chat_action import ChatAction
import httpx
import os
from secure_proxy import SecureProxyClient
import aiofiles

LARGE_FILE = "alik.mp4"

@dp.message(Command("youtube"))
async def youtube(msg: types.Message):
    video = FSInputFile(LARGE_FILE)  
    print(video, "Video")
    await bot.send_chat_action(chat_id=msg.chat.id, action=ChatAction.UPLOAD_VIDEO)
    await bot.send_video(chat_id=msg.chat.id, video=video)



from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp, bot
from  aiogram import types, F
from filters.my_filter import YtCheckLink
import requests
import aiohttp
import time


class YtVideoState(StatesGroup):
    start = State()



@dp.message(F.text, YtCheckLink())
async def get_content(message: types.Message, state: FSMContext):
    url = message.text.strip()
    info = await message.answer("📡 So‘rov bajarilmoqda, kuting...")

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://videoyukla.uz/youtube/media/", params={"yt_url": url})
        data = response.json()
    if data["error"] == True:
        await info.delete()
        await message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!")
        return
    await state.update_data({'data': data})

    btn = InlineKeyboardBuilder()
    btn.button(text="🎥 Video", callback_data="data_video")
    btn.button(text="🎵 Audio", callback_data="data_audio")
    btn.adjust(2)

    # Rasm yuborish
    await message.answer_photo(
        photo=data["thumbnail"],
        caption=data["title"],
        reply_markup=btn.as_markup()
    )

    await state.set_state(YtVideoState.start)
    await info.delete()

os.makedirs("media", exist_ok=True)

@dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
async def get_and_send_media(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Sorov bajarilmoqda kuting...")
    try:
        res = call.data.split("_")[-1]  # "video" yoki "audio"
        state_data = await state.get_data()
        medias = state_data.get("data", {}).get("medias", [])
        title = state_data.get("data", {}).get("title")
        token = state_data.get("data", {}).get("token")
        thumb = state_data.get("data", {}).get("thumbnail")

        if not medias:
            await call.answer("❌ Media topilmadi!")
            return

        first_media = medias[0]

        if not isinstance(first_media, dict):
            print("Error 1")
            await call.message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!1")
            return

        try:
            if res == "video" and "video_url" in first_media:
                video_url = first_media["video_url"]
                try:
                    # First try sending directly
                    await bot.send_video(chat_id=call.message.chat.id, video=video_url, caption=title, supports_streaming=True)

                except Exception as e:
                    print(e, "eeeeeeeeeeeeeee")
                    custom_file_name = f"media/video_{int(time.time())}.mp4"
                    custom_file_name_thumb = f"media/thumb_{int(time.time())}.jpg"

                    thumb = await download_thumb(custom_file_name_thumb, thumb)
                    print(thumb, "thun")

                    download_path1 = await download_file(video_url, custom_file_name, token)
                    print(download_path1, "download_path1")
                    if download_path1:
                        await bot.send_video(chat_id=call.message.chat.id, video=FSInputFile(download_path1), caption=title, supports_streaming=True, thumbnail=FSInputFile(thumb))
                        os.remove(download_path1)
                        os.remove(thumb)
                    else:

                        print("Error 2")
                        await call.message.answer("❌ Video yuklab olinmadi!")
                        
            elif res == "audio" and "audio_url" in first_media:
                audio_url = first_media["audio_url"]
                try:
                    await call.message.answer_audio(audio_url, caption=title)
                except Exception as e:
                    print(e, "eeeeeeeeeeeeeee")
                    custom_file_name = f"media/audio_{int(time.time())}.mp3"
                    download_path1 = await download_file(audio_url, custom_file_name, token)
                    if download_path1:
                        await call.message.answer_audio(
                            audio=FSInputFile(download_path1), 
                            caption=title,
                        )
                        os.remove(download_path1)
                    else:
                        print("Error 3")
                        await call.message.answer("❌ Audio yuklab olinmadi!")
            else:
                await call.message.answer("❌ Noto'g'ri so'rov turi!")
                
        except Exception as e:
            print(f"Error in media sending: {e}")
            await call.message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!error send")

    except Exception as e:
        print(f"General error: {e}")
        await call.message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!general")

async def download_file(url: str, filename: str, token) -> str:
    """URL'dan faylni serverga yuklab olish."""
    try:
        client = SecureProxyClient(proxy_token=token)

        content, status = await client.request(url=url)
        if status != 200:
            print("Yuklab olishda xatolik") 
            return "❌ Xatolik yuz berdi, qayta urinib ko'ring!dowload1"
        
        async with aiofiles.open(filename, "wb") as f:
            await f.write(content)
        print("Yuklandi")
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return "❌ Xatolik yuz berdi, qayta urinib ko'ring!download"
    


async def download_thumb(file_path, url):
    try:
        # Make the HTTP request to fetch the thumbnail
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                async with aiofiles.open(file_path, "wb") as f:
                    # Write the response content (image) to the file
                    await f.write(await response.aread())
                print("Thumbnail yuklandi")
                return file_path
            else:
                print(f"Failed to download thumbnail: {response.status_code}")
                return "❌ Xatolik yuz berdi, qayta urinib ko'ring!thumbnail"
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
        return "❌ Xatolik yuz berdi, qayta urinib ko'ring!thumbnail"