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


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import dp, bot
from  aiogram import types, F
from filters.my_filter import YtCheckLink
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

    if data.get("error"):
        await info.delete()
        return await message.answer("❌ Xatolik yuz berdi, qayta urinib ko'ring!")

    await state.update_data({"data": data})

    btn = InlineKeyboardBuilder()
    btn.button(text="🎥 Video", callback_data="data_video")
    btn.button(text="🎵 Audio", callback_data="data_audio")
    btn.adjust(2)

    # Thumbnail .jpg bilan tugamasa, ro‘yxatdan oxirgi .jpg ni tanlash
    thumb = data.get("thumbnail", "")
    if thumb.endswith(".webp") and "thumbnails" in data:
        jpg_thumbs = [t for t in data["thumbnails"] if t.endswith(".jpg")]
        if jpg_thumbs:
            thumb = jpg_thumbs[-1]  # Oxirgi .jpg

    await message.answer_photo(photo=thumb, caption=data["title"], reply_markup=btn.as_markup())

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

    first_media = next((m for m in medias if m.get("type") == res), None)
    if not first_media:
        return await call.message.answer("❌ Mos media topilmadi!")

    media_url = first_media.get("url")

    try:
        if res == "video":
            try:
                await bot.send_video(call.message.chat.id, video=media_url, caption=title, supports_streaming=True)
            except Exception:
                await send_downloaded_video(call, media_url, title, thumb, token)

        elif res == "audio":
            audio_media = next((m for m in medias if m["type"] == "audio"), None)
            if not audio_media:
                await call.message.answer("❌ Audio topilmadi!")
                return

            audio_url = audio_media["url"]

            try:
                await call.message.answer_audio(audio_url, caption=title)
            except Exception as e:
                print(e, "audio error")
                audio_path = f"media/audio_{int(time.time())}.mp3"
                audio_downloaded = await download_file(audio_url, audio_path, token)

                if audio_downloaded:
                    await call.message.answer_audio(audio=FSInputFile(audio_path), caption=title)
                    os.remove(audio_path)
                else:
                    await call.message.answer("❌ Audio yuklab olinmadi!")

    except Exception as e:
        print(f"Xatolik: {e}")
        await call.message.answer(f"❌ Xatolik yuz berdi, qayta urinib ko'ring!\n{e}")


async def send_downloaded_video(call, url, title, thumb, token):
    """Videoni yuklab olib jo‘natish."""
    video_file = f"media/video_{int(time.time())}.mp4"  
    thumb_file = f"media/thumb_{int(time.time())}.jpg"

    thumb_path, video_path = await asyncio.gather(
        download_thumb(thumb_file, thumb),
        download_file(url, video_file, token),
    )

    if video_path:
        await bot.send_video(
            call.message.chat.id,
            video=FSInputFile(video_path),
            caption=title,
            supports_streaming=True,
            thumbnail=FSInputFile(thumb_path) if thumb_path else None,
        )
        os.remove(video_path)
        if thumb_path:
            os.remove(thumb_path)
    else:
        await call.message.answer("❌ Video yuklab olinmadi!")


async def send_downloaded_video(call, url, title, thumb, token):
    """Videoni yuklab olib jo‘natish."""
    os.makedirs("media", exist_ok=True)  # Papkani tekshir va yarat

    video_file = f"media/video_{int(time.time())}.mp4"  
    thumb_file = f"media/thumb_{int(time.time())}.jpg"

    thumb_path, video_path = await asyncio.gather(
        download_thumb(thumb_file, thumb),
        download_file(url, video_file, token),
    )

    if video_path and os.path.exists(video_path):
        await bot.send_video(
            call.message.chat.id,
            video=FSInputFile(video_path),
            caption=title,
            supports_streaming=True,
            thumbnail=FSInputFile(thumb_path) if thumb_path and os.path.exists(thumb_path) else None,
        )
        os.remove(video_path)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)
    else:
        await call.message.answer("❌ Video yuklab olinmadi!")



async def download_file(url: str, filename: str, token) -> str:
    """URL'dan faylni serverga yuklab olish."""
    try:
        os.makedirs("media", exist_ok=True)  # Papkani tekshir va yarat
        client = SecureProxyClient(proxy_token=token)
        content, status = await client.request(url=url)

        if status != 200:
            print(f"❌ Yuklab olishda xatolik: {status}")
            return None

        async with aiofiles.open(filename, "wb") as f:
            await f.write(content)

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