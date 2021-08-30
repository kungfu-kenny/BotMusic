from telegram.telegram_bot import bot
import telegram.telegram_ui

try:
    bot.polling()
except Exception as e:
    print(f"We faced problems with a main function: {e}")
