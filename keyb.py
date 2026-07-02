# <<<<<<< HEAD
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from lang import transl
from datab import get_user_facts

async def user_lang(user_id, key:str):
    lang = await get_user_facts(user_id, 'language')
    text = transl[lang][key]
    return text

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

ais_style = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='без разницы', callback_data='doesnt_care')],
    ],
    resize_keyboard=True, one_time_keyboard=True
)


async def options(user_id):
    text1 = await user_lang(user_id, 'kick of motivation')
    text2 = await user_lang(user_id, 'tired')
    text3 = await user_lang(user_id, 'call ai')
    options = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text1, callback_data='motivation')],
            [InlineKeyboardButton(text=text2, callback_data='tired')],
            [InlineKeyboardButton(text=text3, callback_data='call_ai')]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return options

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

reminders_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='вода', callback_data='wat_ru'), InlineKeyboardButton(text='', callback_data='food_ru')],
        [InlineKeyboardButton(text='вода', callback_data='sleep_ru'), InlineKeyboardButton(text='', callback_data='')]
    ]
)