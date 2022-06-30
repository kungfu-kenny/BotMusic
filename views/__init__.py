from aiogram import Bot, Dispatcher
from parsers.parser_deezer import ParserDeezer
from config import BotDefault


bot = Bot(BotDefault.key)
dp = Dispatcher(bot)
deezer = ParserDeezer()