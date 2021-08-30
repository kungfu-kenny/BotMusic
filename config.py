import os
from dotenv import load_dotenv

load_dotenv()
######################BLOCK TELEGRAM BASIC#################################

bot_key = os.getenv('BOT_KEY')
chat_id_default = os.getenv('CHAT_ID_DEFAULT')
#######################BLOCK TELEGRAM ROUTES###############################

telegram_start = 'start'
######################BLOCK FOLDERS########################################

folder_db = "db"
folder_storage = "storage"
folder_defaults = "defaults"
folder_telegram = "telegram"