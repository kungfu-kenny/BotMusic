from telegram.telegram_bot import bot
import telegram.telegram_ui
from db.db_creator import SessionCreator
from parsers.parser_default_csv import ParserDefaultCSV


# SessionCreator()
# ParserDefaultCSV(yandex=True, google=True)
ParserDefaultCSV(apple=True)

#TODO add here them bot for telegram
# try:
    # bot.polling()
# except Exception as e:
#     print(f"We faced problems with a main function: {e}")
