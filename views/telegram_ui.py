from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)


def inline_settings(parameter:int=0) -> InlineKeyboardMarkup: 
    """
    Function to return inline settings of the used values
    Input:  parameter = integer which shows tha it is used for a songs or a 
    Output: we developed the inline markup to use it
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Search:',
                    callback_data='0'
                ),
                InlineKeyboardButton(
                    'Songs|✅' if parameter == 0 else 'Songs|❌',
                    callback_data='100'
                ),
                InlineKeyboardButton(
                    'Albums|✅' if parameter == 1 else 'Albums|❌',
                    callback_data='101'
                )
            ],
        ]
    )