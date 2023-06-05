import os

#RETRY BLOCK
MAX_RETRY_COUNT = 3

#PATH_BLOCK
PATH_USE = os.getcwd()
PATH_STORAGE = os.path.join(
    PATH_USE,
    'storage',
)
#'/home/oshevchenko/Projects/BotMusic/storage/'

#CALLBACKS_TELEGRAM_BLOCK
CALLBACK_SONG = 101
CALLBACK_ALBUM = 102