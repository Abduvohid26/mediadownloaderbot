from aiogram import Bot
import asyncio
from data.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

async def main():
    print("Logging out...")
    response = await bot.log_out()
    print("Logout response:", response)

if __name__ == '__main__':
    asyncio.run(main())
