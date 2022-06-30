import imp
import imp
from aiogram import executor
from views import bot, dp
import views.telegram_routes
from db.db_creator import SessionCreator
# from parsers.parser_default_csv import ParserDefaultCSV


# SessionCreator()
# ParserDefaultCSV(yandex=True, google=True)
# ParserDefaultCSV(apple=True)

#TODO add here them bot for telegram
try:
    executor.start_polling(dp, skip_updates=True)
except Exception as e:
    print(f"We faced problems with a main function: {e}")
