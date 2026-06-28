from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)


mainMenu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='start timer')],
        [KeyboardButton(text="today's focus time")],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Yes',  callback_data='work'),
        InlineKeyboardButton(text='No',  callback_data='not_work')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

options = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='im lazy', callback_data='lazy')],
        [InlineKeyboardButton(text='im tired', callback_data='tired')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

start_timer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Yes',  callback_data='start_timer'),
        InlineKeyboardButton(text='No',  callback_data='dont_start_timer')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

options_timer = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='pause',  callback_data='pause_timer'),
        InlineKeyboardButton(text='stop',  callback_data='stop_timer')]
    ],
    resize_keyboard=True, one_time_keyboard=True
)
choose_language = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="set_lang_ru"), InlineKeyboardButton(text="English", callback_data="set_lang_en")]
    ]
)