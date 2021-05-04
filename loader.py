from config import BOT_TOKEN
from aiogram import Bot
from aiogram_tools import Dispatcher
from aiogram.contrib.fsm_storage.mongo import MongoStorage
import logging
from database_api import MongoDB

bot = Bot(BOT_TOKEN)
storage = MongoStorage(db_name='iFeedbackBot_fsm')
dp = Dispatcher(bot, storage=storage)

db = MongoDB('iFeedbackBot')
messages = db.messages

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('bot')
