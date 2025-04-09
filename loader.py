from aiogram import Bot,Dispatcher
from data.config import BOT_TOKEN
# Import Database Class
from utils.db_api.sqlite import Database
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

api_server = TelegramAPIServer.from_base("http://localhost:8081", is_local=True)

bot=Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=AiohttpSession(api=api_server))
dp=Dispatcher(storage=MemoryStorage())
# Create database file
db = Database(path_to_db='data/main.db')