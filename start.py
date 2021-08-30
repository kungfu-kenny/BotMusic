from telegram.telegram_bot import bot
import telegram.telegram_ui
from db.db_creator import SessionCreator

SessionCreator()
try:
    bot.polling()
except Exception as e:
    print(f"We faced problems with a main function: {e}")
