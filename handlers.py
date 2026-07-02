
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from datetime import date, timedelta, datetime
import asyncio
import time
from datab import (add_user_facts, add_user_stats, get_user_facts, add_focus_time, get_user_time,
                   get_user_stats, add_time_start, get_time_start, get_all_user_facts,
                   add_ai_style, get_ai_style, get_ai_responses, add_history, clear_history)
import keyb as kb
from lang import transl
from ai import respond_to_motivation, respond_to_tired, respond_to_call
from keyb import options

user = Router()
user_focus_time = {}

 #classes for questions
class UserInfo(StatesGroup):
    waiting_for_goal = State()
    waiting_for_motivation = State()
    waiting_for_previousSuccesses = State()
    waiting_for_dailyTime = State()
    is_with_ai = State()
    procrastination_level = State()
    preferred_style = State()
    final = State()

async def message_in_user_lang(message: types.Message,user_id, key:str, reply_markup=None):
    lang = await get_user_facts(user_id, 'language')
    if lang is None:
        lang = 'en'
    text = transl[lang][key]
    await message.answer(text, reply_markup=reply_markup)

async def text_in_lang(user_id, key:str):
    lang = await get_user_facts(user_id, 'language')
    text = transl[lang][key] or transl['en'][key]
    return text

# set language
@user.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Choose your language / Выберите язык ', reply_markup = kb.choose_language)

@user.callback_query(F.data.startswith('set_lang_'))
async def language_chosen(callback: types.CallbackQuery):
    lang_code = callback.data.split('_')[-1]
    user_id = callback.from_user.id
    await add_user_facts(user_id, 'language', lang_code)
    await message_in_user_lang(callback.message,user_id, 'welcome', reply_markup=kb.mainMenu)

# questions to form users portrait
@user.message(Command('ready'))
async def questions_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message_in_user_lang(message,user_id, '1question')
    await state.set_state(UserInfo.waiting_for_goal)

@user.message(UserInfo.waiting_for_goal)
async def answer_goal(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'the goal: ', user_answer)
    await message_in_user_lang(message,user_id, '2question')
    await state.set_state(UserInfo.waiting_for_motivation)

@user.message(UserInfo.waiting_for_motivation)
async def answer_motivation(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'the motivation to achieve it: ', user_answer)
    await message_in_user_lang(message, user_id, '3question')
    await state.set_state(UserInfo.waiting_for_dailyTime)

@user.message(UserInfo.waiting_for_dailyTime)
async def answer_dailytime(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'what the user already did to achieve it: ', user_answer)
    await message_in_user_lang(message, user_id, '4question')
    await state.set_state(UserInfo.procrastination_level)

@user.message(UserInfo.procrastination_level)
async def how_much_procrastination(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'how much time daily the user is ready to spend for their goal: ', user_answer)
    await message_in_user_lang(message, user_id, '5question')
    await state.set_state(UserInfo.preferred_style)

@user.message(UserInfo.preferred_style)
async def done_with_questions(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_answer = message.text
    await add_user_facts(user_id, 'how much and how exactly the user procrastinates: ', user_answer)
    await message_in_user_lang(message, user_id, '6question', reply_markup=kb.ais_style)
    await state.set_state(UserInfo.final)

#ai default style
@user.callback_query(F.data=='doesnt_care')
async def no_style(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message_in_user_lang(message, user_id, 'no ai style')
    await state.clear()

@user.message(UserInfo.final)
async def done_with_questions(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_answer = message.text
    await add_ai_style(user_id, user_answer)
    await message_in_user_lang(message, user_id, 'done with questions')
    await state.clear()

@user.message(Command('water'))
async def water(message: types.Message):
    user_id = message.from_user.id
    if await get_user_stats(user_id, 'water_reminder')=='ON':
        await add_user_stats(user_id, 'water_reminder', 'OFF')
        await message_in_user_lang(message, user_id, 'water_off')
    else:
        await add_user_stats(user_id, 'water_reminder', 'ON')
        await message_in_user_lang(message, user_id, 'water_on')

@user.message(Command('stretch'))
async def stretch(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await get_user_facts(user_id, 'stretch_reminder')=='ON':
        await add_user_stats(user_id, 'stretch_reminder', 'OFF')
        await message_in_user_lang(message, user_id, 'stretch_off')
    else:
        await add_user_stats(user_id, 'stretch_reminder', 'ON')
        await message_in_user_lang(message, user_id, 'stretch_on')

@user.message(F.data=='start timer')
async def start_timer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await add_user_stats(user_id, 'timer', 'ON')


#callbacks
@user.callback_query(F.data=='not_work')
async def why(callback: CallbackQuery):
    user_id = callback.from_user.id
    option = await options(user_id)
    message = callback.message
    await message_in_user_lang(message, user_id, 'why', reply_markup=option)
    await callback.answer()

@user.callback_query(F.data=='motivation')
async def motivation(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = await get_ai_responses(user_id, 'motivation')
    if text:
        await callback.message.answer(text)
    else:
        respond = await respond_to_motivation(user_id)
        await callback.message.answer(respond)

@user.callback_query(F.data=='tired')
async def tired(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = await get_ai_responses(user_id, 'tired')
    if text:
        await callback.message.answer(text)
    else:
        respond = await respond_to_tired(user_id)
        await callback.message.answer(respond)

@user.callback_query(F.data=='call_ai')
async def call_ai(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    user_id = message.from_user.id
    users_message = message.text
    text = ''' (чтобы остановить чат и стереть историю нажми /clear)
Я здесь. Расскажи, что тебя беспокоит? Может, есть задача, которая кажется слишком большой? Давай попробуем разбить её на кусочки вместе.'''
    await add_history(user_id, 'USER', users_message)
    await callback.message.answer(text)
    await state.set_state(UserInfo.is_with_ai)
    await callback.answer()

@user.message(UserInfo.is_with_ai)
async def chat_with_ai(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    users_message = message.text
    await add_history(user_id, 'USER', users_message)
    response = await respond_to_call(user_id)
    await message.answer(response)
@user.message(Command('clear'))
async def clear(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await clear_history(user_id)
    await state.clear()
    await message_in_user_lang(message, user_id, 'clear')


@user.callback_query(F.data=='work')
async def mb_timer(callback: CallbackQuery):
    await message_in_user_lang(callback.message, callback.from_user.id, 'start timer?', reply_markup=kb.start_timer)
    await callback.answer()


async def smart_reminder(message: types.Message, user_id, start_time):
    await asyncio.sleep(90*60)
    is_timer_on = await get_user_stats(user_id, 'timer')
    last_start = await get_time_start(user_id)
    if is_timer_on=='ON' and last_start==start_time:
        await message_in_user_lang(message, user_id, 'make a break')

#timer
@user.callback_query(F.data=='start_timer')
async def start_timer(callback: CallbackQuery):
    user_id = callback.from_user.id
    message = callback.message
    current_time = time.time()
    await message_in_user_lang(message, user_id, 'start timer', reply_markup=kb.options_timer)
    await add_user_stats(user_id, 'timer', 'ON')
    await add_time_start(user_id, current_time)
    asyncio.create_task(smart_reminder(message, user_id, current_time))
    await callback.answer()

@user.message(F.text=='start timer')
async def start_timer(message: types.Message):
    user_id = message.from_user.id
    await message_in_user_lang(message, user_id, 'start timer', reply_markup=kb.options_timer)
    await add_user_stats(user_id, 'timer', 'ON')
    await add_time_start(user_id, time.time())

def format_seconds(total_seconds):
    total_seconds = int(total_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours != 0:
        return f"{hours} h. {minutes} min. {seconds} s."
    return f"{minutes} min. {seconds} s."

@user.callback_query(F.data == 'stop_timer')
async def stop_timer(callback: CallbackQuery):
    user_id = callback.from_user.id
    await add_user_stats(user_id, 'timer', 'OFF')
    time_of_start = await get_time_start(user_id)
    if time_of_start:
        total_seconds = time.time() - time_of_start
        delta = timedelta(seconds=total_seconds)
        tot_time = int(delta.total_seconds())
        today = datetime.now().strftime('%Y-%m-%d')
        user_id = callback.from_user.id
        text_template = await text_in_lang(user_id, 'focus time')
        text = text_template.format(format_seconds(total_seconds))
        await callback.message.answer(text)
        await add_focus_time(user_id, today, tot_time)

# @user.message(Command('TotalFocus'))
@user.message(F.text == "today's focus time")
async def total_focus(message: types.Message):
    user_id = message.from_user.id
    today = datetime.now().strftime('%Y-%m-%d')
    focus_time = await get_user_time(user_id, today)
    focus_time_2 = format_seconds(focus_time)
    if focus_time:
        text = await text_in_lang(user_id, 'total focus')
        await message.answer(f"{text} {focus_time_2}")
    else:
        await message_in_user_lang(message, user_id, 'no focus')

