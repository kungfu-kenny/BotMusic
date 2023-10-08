import logging
from aiogram import executor
from models.database import develop_database_basic
from telegram.telegram_usage import dp
from telegram.telegram_ui import *


if __name__ == "__main__":
    # Configure logging
    develop_database_basic()
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)