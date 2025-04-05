# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from loader import dp, bot
# from  aiogram import types, F
# from filters.my_filter import YtCheckLink
# import requests
# class YtVideoState(StatesGroup):
#     start = State()


# @dp.message(F.text, YtCheckLink())
# async def get_content(message: types.Message, state: FSMContext):
#     url = message.text.strip()
#     info = await message.answer("Sorov Bajarilmoqda Kuting...")

#     response = requests.post("https://videoyukla.uz/youtube/media/", data={"url": url, "k": "240"})
#     print(response, 'res')
#     data = response.json()
#     await state.update_data({'data': data})
#     btn = InlineKeyboardBuilder()
#     btn.button(text="Video", callback_data="data_video")
#     btn.button(text="Audio", callback_data="data_audio")
#     btn.adjust(2)
#     await message.answer_photo(
#             photo=data["thumb"],
#             caption=data["title"],
#             reply_markup=btn.as_markup()
#         )
#     await state.set_state(YtVideoState.start)
#     await info.delete()


#     # if not data.get("error"):
#     #     await info.delete()
#     #     await state.update_data({"data": data})
#     #     print(data["thumbnail"], "thub", data)
#     #     btn = InlineKeyboardBuilder()
#     #     btn.button(text="Video", callback_data="data_video")
#     #     btn.button(text="Audio", callback_data="data_audio")
#     #     btn.adjust(2)
#     #
#     #     await message.answer_photo(
#     #         photo=data["thumbnail"],
#     #         caption=data["title"],
#     #         reply_markup=btn.as_markup()
#     #     )
#     #     await state.set_state(YtVideoState.start)
#     # else:
#     #     await info.delete()
#     #     await message.answer("Xatolik yuz berdi, qayta urinib ko'ring.")


# @dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
# async def get_and_send_media(call: types.CallbackQuery, state: FSMContext):
#     res = call.data.split("_")[-1]
#     state_data = await state.get_data()
#     try:
#         if res == "video":
#             print(state_data["data"]["video_download_url"])
#             video = state_data["data"]["video_download_url"]
#             title = state_data["data"]["title"]
#             await call.message.answer_video(video=video, caption=title)
#             return
#         else:
#             print(state_data["data"]["audio_download_url"])
#             audio = state_data["data"]["audio_download_url"]
#             title = state_data["data"]["title"]
#             await call.message.answer_audio(audio=audio, caption=title)
#             return
#     except Exception as e:
#         print("Error:", e)
#         await call.message.answer(text="Xatolik yuz berdi qayta urinib ko'ring")
#     # @dp.callback_query(YtVideoState.start, lambda query: query.data.startswith("data_"))
# # async def get_and_send_media(call: types.CallbackQuery, state: FSMContext):
# #     res = call.data.split("_")[-1]
# #     state_data = await state.get_data()
# #     print(state_data, "data")
# #     medias = state_data.get("data", {}).get("medias", [])
# #     title = state_data.get("data", {}).get("title")
# #
# #     if not medias:
# #         await call.answer("Media topilmadi!")
# #         return
# #
# #     for data in medias:
# #         if res == "video" and data.get("type") == "video" and not data.get("is_audio") and data.get("ext") == "mp4":
# #             await call.message.answer_video(data["url"], caption=title)
# #             return
# #
# #         if res == "audio" and data.get("type") == "audio" and data.get("is_audio") and data.get("ext") in ["weba", "mp3"]:
# #             await call.message.answer_audio(data["url"], caption=title)
# #             return
# #
# #     await call.answer("Mos media topilmadi!")
# #     await state.clear()

