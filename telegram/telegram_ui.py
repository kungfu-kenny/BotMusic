from .telegram_bot import bot
from config import telegram_start

@bot.message_handler(commands=[telegram_start])
def start_message(message):
    bot.send_message(message.chat.id, telegram_start)
