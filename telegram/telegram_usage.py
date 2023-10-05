from aiogram import (
    Bot,
    Dispatcher,
)
from config import API_TOKEN


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)
