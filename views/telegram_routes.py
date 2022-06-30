from pprint import pp, pprint
from aiogram import types
from . import (
    dp, 
    bot, 
    deezer,
)
from .telegram_ui import inline_settings
from config import Telegram




@dp.message_handler(commands=[Telegram.start])
async def start_message(message):
    """
    Route which is dedicated to work with an entry point to the user
    Input:  message = aiogram message type which was previously given
    Output: text with an explanation of all of it and returnal of the values
    """
    #TODO add here the message work & message menu
    print(message)
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    await message.answer('telegram_start')

@dp.message_handler(commands=[Telegram.settings])
async def work_settings(message):
    """
    Route which is dedicated to work with a settings to the selected users
    Input:  message = aiogram message type which was used as a command
    Output: inline keyboard to change values for all of the selected values
    """
    #TODO add here the message settings menu
    search_preference = 0 #TODO add here the db function to all of it
    return await message.answer(
        'Your settings:', 
        reply_markup=inline_settings(search_preference)
    )

@dp.message_handler(commands=[Telegram.history])
async def work_history(message):
    """
    Route which is dedicated to work with a history of the selected values to it
    Input:  message = aiogram message type which was used previously as a command
    Output: inline keyboard for the search previously
    """
    #TODO add here the development of the history search
    print(message)
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

@dp.message_handler()
async def search(message: types.Message):
    #TODO add here the search values from the different searcher
    search_preference = 0 #TODO add here the db function to all of it
    list_deezer = await deezer.produce_search_selected(message.text, search_preference)
    # pprint(list_deezer)
    await message.answer(message.text)

#TODO add this later
# @dp.callback_query_handler()
# async def change_search_type():
#     pass