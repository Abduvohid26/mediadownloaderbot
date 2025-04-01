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
        response = await client.post("http://95.169.205.213:8080/instagram/media", data={"url": url}, timeout=15)
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


from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

class YtVideoState(StatesGroup):
    start = State()


@dp.message(F.text, YtCheckLink())
async def get_content(message: types.Message, state: FSMContext):
    url = message.text.strip()
    info = await message.answer("Sorov Bajarilmoqda Kuting...")

    response = requests.post("http://95.169.205.213:8080/yt/media", data={"url": url})
    data = response.json()

    if not data.get("error"):
        await info.delete()
        await state.update_data({"data": data})

        btn = InlineKeyboardBuilder()
        btn.button(text="Video", callback_data="data_video")
        btn.button(text="Audio", callback_data="data_audio")
        btn.adjust(2)

        await message.answer_photo(
            photo=data["thumbnail"],
            caption=data["title"],
            reply_markup=btn.as_markup()
        )
        await state.set_state(YtVideoState.start)
    else:
        await info.delete()
        await message.answer("Xatolik yuz berdi, qayta urinib ko'ring.")


@dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
async def get_and_(call: types.CallbackQuery, state: FSMContext):
    res = call.data.split("_")[-1]
    state_data = await state.get_data()
    medias = state_data.get("data", {}).get("medias", [])
    title = state_data.get("data", {}).get("title")
    if not medias:
        await call.answer("Media topilmadi!")
        return

    for data in medias:
        if (
                (res == "video" and data.get("type") == "video" and not data.get("is_audio")) or
                (res == "audio" and data.get("type") == "audio" and data.get("is_audio"))
        ):
            if res == "video":
                await call.message.answer_video(data["url"], caption=title)
            else:
                await call.message.answer_audio(data["url"], caption=title)
            return

    await call.answer("Mos media topilmadi!")
    await state.clear()