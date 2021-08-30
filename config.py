import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv('BOT_KEY')
chat_id_default = os.getenv('CHAT_ID_DEFAULT')

telegram_start = 'start'