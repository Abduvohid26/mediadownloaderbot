import handlers,middlewares
from loader import dp,bot,db
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start,shutdown
from utils.set_botcommands import commands

# Info
import logging
import sys

import os
import asyncio

WATCH_FOLDER = "media"
CHECK_INTERVAL = 1  # seconds


async def rename_part_files():
    while True:
        # print("salom1")
        for filename in os.listdir(WATCH_FOLDER):
            if filename.endswith(".mp3.part"):
                part_path = os.path.join(WATCH_FOLDER, filename)
                final_path = os.path.join(WATCH_FOLDER, filename.replace(".mp3.part", ".mp3"))

                if not os.path.exists(final_path):  # agar .mp3 fayl hali mavjud bo'lmasa
                    try:
                        os.rename(part_path, final_path)
                        print(f"Renamed: {filename} -> {os.path.basename(final_path)}")
                    except Exception as e:
                        print(f"Xatolik {filename} faylni o'zgartirishda: {e}")
        await asyncio.sleep(CHECK_INTERVAL)


async def main():
    try:
        # asyncio.create_task(rename_part_files())
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands,scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        # Create Users Table
        try:
            db.create_table_users()
        except:
            pass
        #############################
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    # asyncio.run(rename_part_files())
