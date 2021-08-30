from telegram.telegram_bot import bot
from telegram.telegram_ui import start_message

try:
    bot.polling()
except Exception as e:
    print(f"We faced problems with a main function: {e}")
