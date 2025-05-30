from aiogram.filters import Command
from aiogram.types import FSInputFile
from loader import bot, dp
from aiogram import types
from aiogram.enums.chat_action import ChatAction
import httpx
import os
from secure_proxy import SecureProxyClient
import aiofiles
import asyncio
import yt_dlp

from concurrent.futures import ThreadPoolExecutor
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp, bot
from  aiogram import types, F
from filters.my_filter import YtCheckLink
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
import time



class YtVideoState(StatesGroup):
    start = State()


@dp.message(F.text, YtCheckLink())
async def get_content(message: types.Message, state: FSMContext):
    url = message.text.strip()
    info = await message.answer("📡 So‘rov bajarilmoqda, kuting...")

    async with httpx.AsyncClient(timeout=100) as client:
        try:
            response = await client.get("https://videoyukla.uz/youtube/media/", params={"yt_url": url})
            data = response.json()
        except httpx.RequestError as e:
            await info.delete()
            return await message.answer(f"❌ So'rov xatolik: {e}")
    # print(data, "DATA")
    if data.get("error"):
        await info.delete()
        return await message.answer(f"❌ Xatolik yuz berdi, qayta urinib ko'ring")

        # return await message.answer(f"❌ Xatolik yuz berdi, qayta urinib ko'ring!\n{data}")

    await state.update_data({"data": data})

    btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎥 Video", callback_data="data_video"),
         InlineKeyboardButton(text="🎵 Audio", callback_data="data_audio")]
    ])

    thumb = data.get("thumbnail", "")
    if thumb.endswith(".webp") and "thumbnails" in data:
        thumb = next((t for t in data["thumbnails"] if t.endswith(".jpg")), "")

    await message.answer_photo(photo=thumb, caption=data["title"], reply_markup=btn)
    await state.set_state(YtVideoState.start)
    await info.delete()


@dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
async def get_and_send_media(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📡 So‘rov bajarilmoqda, kuting...")

    res = call.data.split("_")[-1]  # "video" yoki "audio"
    state_data = await state.get_data()
    medias = state_data.get("data", {}).get("medias", [])
    title = state_data.get("data", {}).get("title", "Video")
    token = state_data.get("data", {}).get("token")
    thumb = state_data.get("data", {}).get("thumbnail")

    if not medias:
        return await call.answer("❌ Media topilmadi!")

    media_type = next((m for m in medias if m.get("type") == res), None)
    if not media_type:
        return await call.message.answer(f"❌ {res.capitalize()} topilmadi!")

    media_url = medias[0].get("url")

    try:
        if res == "video":
            await send_media(call, media_url, title, thumb, token, media_type=media_type)
        # elif res == "video":
        #     print("audio1")
        else:
            await send_audio(call, media_url, title, token, media_type=media_type)
    except Exception as e:
        error = str(e)
        if "[Errno 2] No such file or directory:" in error:
            print(e, "E")
            return
        await call.message.answer(f"❌ Xatolik yuz berdi, qayta urinib ko'ring!\n{e}")


async def send_media(call, url, title, thumb, token, media_type):
    try:
        await bot.send_video(call.message.chat.id, video=url, caption=title, supports_streaming=True)
    except Exception:
        await send_downloaded_media(call, url, title, thumb, token, media_type)

from .get_proxy import _get_proxy_url

import subprocess

async def send_audio(call, url, title, token, media_type):
    """Audio faylni yuborish va xatoliklarni ushlash"""

    # try:
    #     # proxy_data = await _get_proxy_url(proxy_token=token)
    #
    #
    #     # print(call.message.chat.id, "ID")
    #     # res_path = await download_audio(url=url,output_path=audio_path, proxy_config=proxy_data)
    #     res_path = await  download_file(url=url, filename=audio_path, token=token)
    #     print(res_path, "RES PATH")
    #
    #     try:
    #         await call.message.answer_audio(audio=FSInputFile(res_path), caption=title)
    #     except Exception as e:
    #         print(f"Audio yuborishda xato: {e}")
    #         return {"success": False, "error": f"Audio yuborishda xato: {e}"}
    #
    #     if os.path.exists(audio_path):
    #         os.remove(audio_path)
    #
    #     return {"success": True, "message": "Audio muvaffaqiyatli yuborildi"}
    #
    # except Exception as e:
    #     print(f"Xatolik yuz berdi: {e}")
    #     return {"success": False, "error": f"Xatolik yuz berdi: {e}"}
    file_path = f"media/{media_type['type']}_{int(time.time())}.mp4"

    os.makedirs("media", exist_ok=True)
    print("salom")
    video_path = await download_file(url, file_path, token)
    print(video_path, "video_path")
    audio_path = f"media/audio_{int(time.time())}.mp3"
    await extract_audio_on_video(video_path, audio_path)
    if os.path.exists(audio_path):
        await call.message.answer_audio(audio=FSInputFile(audio_path), caption=title)
        os.remove(audio_path)
    else:
        await call.message.answer(text="Audio yuborishda xatolik")
        return



async def extract_audio_on_video(video_path, audio_path):
    try:
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "libmp3lame",
            "-ab", "192k", "-ar", "44100",
            "-y", audio_path
        ], check=True)
        print(f"✅ Audio saved: {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Xatolik: {e}")












async def send_downloaded_media(call, url, title, thumb, token, media_type):
    file_path = f"media/{media_type['type']}_{int(time.time())}.mp4"
    thumb_path = f"media/thumb_{int(time.time())}.jpg"

    os.makedirs("media", exist_ok=True)

    thumb_path, video_path = await asyncio.gather(
        download_thumb(thumb_path, thumb),
        download_file(url, file_path, token),
    )
    print(thumb_path, "thumb")

    if video_path and os.path.exists(video_path):
        await bot.send_video(
            call.message.chat.id,
            thumbnail=FSInputFile(thumb_path),
            video=FSInputFile(video_path),
            caption=title,
            supports_streaming=True,
        )
        os.remove(video_path)
        if thumb_path:
            os.remove(thumb_path)
    else:
        await call.message.answer("❌ Video yuklab olinmadi!")


async def download_file(url: str, filename: str, token) -> str:
    """URL'dan faylni serverga yuklab olish."""
    try:
        client = SecureProxyClient(proxy_token=token)
        content, status = await client.request(url=url)

        if status != 200:
            return None

        os.makedirs("media", exist_ok=True)
        async with aiofiles.open(filename, "wb") as f:
            print("cpn")
            await f.write(content)
        print("ass")
        return filename
    except Exception as e:
        print(f"❌ Fayl yuklab olishda xatolik: {e}")
        return None



async def download_thumb(file_path, url):
    """Thumbnail rasmni yuklab olish."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(await response.aread())
                return file_path
    except Exception as e:
        print(f"❌ Thumbnail yuklab olishda xatolik: {e}")

    return None



def sync_download_audio(url: str, output_path: str, proxy_config=None):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    if proxy_config:
        options["proxy"] = proxy_config

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])
    print("salom")




async def download_audio(url: str, output_path: str, proxy_config):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, sync_download_audio, url, output_path, proxy_config)

    return output_path



from aiogram.filters import CommandStart
from loader import dp, bot
from aiogram import types, F
import requests
from filters.my_filter import TiktokCheckLink
from aiogram.enums.chat_action import ChatAction
import httpx
from aiogram.types.input_file import InputFile, FSInputFile
import io
from aiogram.types import BufferedInputFile


@dp.message(F.text, TiktokCheckLink())
async def handle_tiktok_link(message: types.Message):
    await message.answer("⏳ Video yuklanmoqda, iltimos kuting...")
    url = message.text.strip()

    # Yuklash holatini ko'rsatish
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            api_url = "https://videoyukla.uz/tiktok/media"
            response = await client.get(api_url, params={"tk_url": url})
            data = response.json()
            if data.get("error"):
                await bot.send_message(message.chat.id, "Xatolik yuz berdi qayta urinib ko'ring")
            download_url = response.json()["medias"][0]["download_url"]
            filename = f"media/{download_url.split('/')[-1].split('?')[0]}"

            video_response = await client.get(download_url)

            with open(filename, "wb") as f:
                f.write(video_response.content)
            await bot.send_video(chat_id=message.chat.id, video=FSInputFile(filename))
    except Exception as e:
        await message.answer(f"❌ Kutilmagan xatolik: {str(e)}")



# async def download_audio(url: str, output_path: str, proxy_config, chat_id):
#     loop = asyncio.get_event_loop()
#     with ThreadPoolExecutor() as executor:
#         download_task = loop.run_in_executor(executor, sync_download_audio, url, output_path, proxy_config)

        # send_task = send_audio_(output_path, chat_id)

        # await asyncio.gather(download_task, send_task)

    # return output_path


# async def download_youtube_audio(url):
#     options = {
#         'format': 'bestaudio/best',
#         'outtmpl': 'output/mp3/%(id)s.%(ext)s',
#         'noplaylist': True,
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
#
#     with ytd.YoutubeDL(options) as ytdl:
#         result = ytdl.extract_info(url, download=True)
#         file_path = f"output/mp3/{result['id']}.mp3"
#
#         if not os.path.exists(file_path):
#             return None
#
#         return file_path


# class YtVideoState(StatesGroup):
#     start = State()



# @dp.message(F.text, YtCheckLink())
# async def get_content(message: types.Message, state: FSMContext):
#     url = message.text.strip()
#     info = await message.answer("📡 So‘rov bajarilmoqda, kuting...")

#     async with httpx.AsyncClient(timeout=30) as client:
#         response = await client.get("https://videoyukla.uz/youtube/media/", params={"yt_url": url})
#         data = response.json()

#     if data.get("error"):
#         await info.delete()
#         return await message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!\n" \
#         f"{data}")

#     await state.update_data({"data": data})

#     btn = InlineKeyboardBuilder()
#     btn.button(text="🎥 Video", callback_data="data_video")
#     btn.button(text="🎵 Audio", callback_data="data_audio")
#     btn.adjust(2)

#     # Thumbnail .jpg bilan tugamasa, ro‘yxatdan oxirgi .jpg ni tanlash
#     thumb = data.get("thumbnail", "")
#     if thumb.endswith(".webp") and "thumbnails" in data:
#         jpg_thumbs = [t for t in data["thumbnails"] if t.endswith(".jpg")]
#         if jpg_thumbs:
#             thumb = jpg_thumbs[-1]  # Oxirgi .jpg

#     await message.answer_photo(photo=thumb, caption=data["title"], reply_markup=btn.as_markup())

#     await state.set_state(YtVideoState.start)
#     await info.delete()


# @dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
# async def get_and_send_media(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer("📡 So‘rov bajarilmoqda, kuting...")

#     res = call.data.split("_")[-1]  # "video" yoki "audio"
#     state_data = await state.get_data()
#     medias = state_data.get("data", {}).get("medias", [])
#     title = state_data.get("data", {}).get("title", "Video")
#     token = state_data.get("data", {}).get("token")
#     thumb = state_data.get("data", {}).get("thumbnail")

#     if not medias:
#         return await call.answer("❌ Media topilmadi!")

#     first_media = next((m for m in medias if m.get("type") == res), None)
#     if not first_media:
#         return await call.message.answer("❌ Mos media topilmadi!")

#     media_url = first_media.get("url")

#     try:
#         if res == "video":
#             try:
#                 await bot.send_video(call.message.chat.id, video=media_url, caption=title, supports_streaming=True)
#             except Exception:
#                 await send_downloaded_video(call, media_url, title, thumb, token)

#         elif res == "audio":
#             audio_media = next((m for m in medias if m["type"] == "audio"), None)
#             if not audio_media:
#                 await call.message.answer("❌ Audio topilmadi!")
#                 return

#             audio_url = audio_media["url"]

#             try:
#                 await call.message.answer_audio(audio_url, caption=title)
#             except Exception as e:
#                 print(e, "audio error")
#                 audio_path = f"media/audio_{int(time.time())}.mp3"
#                 audio_downloaded = await download_file(audio_url, audio_path, token)

#                 if audio_downloaded:
#                     await call.message.answer_audio(audio=FSInputFile(audio_path), caption=title)
#                     os.remove(audio_path)
#                 else:
#                     await call.message.answer("❌ Audio yuklab olinmadi!")

#     except Exception as e:
#         print(f"Xatolik: {e}")
#         await call.message.answer(f"❌ Xatolik yuz berdi, qayta urinib ko'ring!\n{e}")


# async def send_downloaded_video(call, url, title, thumb, token):
#     """Videoni yuklab olib jo‘natish."""
#     video_file = f"media/video_{int(time.time())}.mp4"  
#     thumb_file = f"media/thumb_{int(time.time())}.jpg"

#     thumb_path, video_path = await asyncio.gather(
#         download_thumb(thumb_file, thumb),
#         download_file(url, video_file, token),
#     )
#     if video_path and os.path.exists(video_path):
#         await bot.send_video(
#             call.message.chat.id,
#             video=FSInputFile(video_path),
#             caption=title,
#             supports_streaming=True,
#             thumbnail=FSInputFile(thumb_path) if thumb_path and os.path.exists(thumb_path) else None,
#         )
#     else:
#         await call.message.answer("❌ Video yuklab olinmadi yoki fayl bo‘sh.")


#     # if video_path:
#     #     await bot.send_video(
#     #         call.message.chat.id,
#     #         video=FSInputFile(video_path),
#     #         caption=title,
#     #         supports_streaming=True,
#     #         thumbnail=FSInputFile(thumb_path) if thumb_path else None,
#     #     )
#     #     os.remove(video_path)
#     #     if thumb_path:
#     #         os.remove(thumb_path)
#     # else:
#     #     await call.message.answer("❌ Video yuklab olinmadi!")


# async def send_downloaded_video(call, url, title, thumb, token):
#     """Videoni yuklab olib jo‘natish."""
#     os.makedirs("media", exist_ok=True)  # Papkani tekshir va yarat

#     video_file = f"media/video_{int(time.time())}.mp4"  
#     thumb_file = f"media/thumb_{int(time.time())}.jpg"

#     thumb_path, video_path = await asyncio.gather(
#         download_thumb(thumb_file, thumb),
#         download_file(url, video_file, token),
#     )

#     if video_path and os.path.exists(video_path):
#         await bot.send_video(
#             call.message.chat.id,
#             video=FSInputFile(video_path),
#             caption=title,
#             supports_streaming=True,
#             thumbnail=FSInputFile(thumb_path) if thumb_path and os.path.exists(thumb_path) else None,
#         )
#         os.remove(video_path)
#         if thumb_path and os.path.exists(thumb_path):
#             os.remove(thumb_path)
#     else:
#         await call.message.answer("❌ Video yuklab olinmadi!")



# async def download_file(url: str, filename: str, token) -> str:
#     """URL'dan faylni serverga yuklab olish."""
#     try:
#         os.makedirs("media", exist_ok=True)  # Papkani tekshir va yarat
#         client = SecureProxyClient(proxy_token=token)
#         content, status = await client.request(url=url)

#         if status != 200:
#             print(f"❌ Yuklab olishda xatolik: {status}")
#             return None

#         async with aiofiles.open(filename, "wb") as f:
#             await f.write(content)

#         return filename
#     except Exception as e:
#         print(f"❌ Fayl yuklab olishda xatolik: {e}")
#         return None


# async def download_thumb(file_path, url):
#     """Thumbnail rasmni yuklab olish."""
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             if response.status_code == 200:
#                 async with aiofiles.open(file_path, "wb") as f:
#                     await f.write(await response.aread())
#                 return file_path
#     except Exception as e:
#         print(f"❌ Thumbnail yuklab olishda xatolik: {e}")

#     return None


