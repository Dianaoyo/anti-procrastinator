from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.command import CommandStart
from datetime import date, timedelta, datetime
import time
from datab import add_user_facts, add_reminder, get_user_facts, add_focus_time, get_user_time
import keyb as kb
from lang import transl

user = Router()
user_focus_time = {}

 #classes for questions
class UserInfo(StatesGroup):
    waiting_for_goal = State()
    waiting_for_motivation = State()
    waiting_for_previousSuccesses = State()
    waiting_for_dailyTime = State()
    procrastination_level = State()
    preferred_style = State()
    final = State()

async def message_in_user_lang(message: types.Message,user_id, key:str):
    # user_id = message.from_user.id
    lang = await get_user_facts(user_id, 'language')
    text = transl[lang][key]
    await message.answer(text)

@user.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Choose your language / Выберите язык ', reply_markup = kb.choose_language)

@user.callback_query(F.data.startswith('set_lang_'))
async def language_chosen(callback: types.CallbackQuery):
    lang_code = callback.data.split('_')[-1]
    user_id = callback.from_user.id
    await add_user_facts(user_id, 'language', lang_code)
    lang_in_db = await get_user_facts(user_id, 'language')
    await message_in_user_lang(callback.message,callback.from_user.id, 'welcome')

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
    await add_user_facts(user_id, 'goal', user_answer)
    await message_in_user_lang(message,user_id, '2question')
    await state.set_state(UserInfo.waiting_for_motivation)

@user.message(UserInfo.waiting_for_motivation)
async def answer_motivation(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'motivation', user_answer)
    await message_in_user_lang(message, user_id, '3question')
    await state.set_state(UserInfo.waiting_for_dailyTime)

@user.message(UserInfo.waiting_for_dailyTime)
async def answer_dailytime(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'what user did to achieve it', user_answer)
    await message_in_user_lang(message, user_id, '4question')
    await state.set_state(UserInfo.procrastination_level)

@user.message(UserInfo.procrastination_level)
async def how_much_procrastination(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_id = message.from_user.id
    await add_user_facts(user_id, 'how much time the user is ready to spend for their goal', user_answer)
    await message_in_user_lang(message, user_id, '5question')
    await state.set_state(UserInfo.preferred_style)

@user.message(UserInfo.preferred_style)
async def done_with_questions(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_answer = message.text
    await add_user_facts(user_id, 'how much procrastination ', user_answer)
    await message_in_user_lang(message, user_id, '6question')
    await state.set_state(UserInfo.final)

@user.message(UserInfo.final)
async def done_qith_questions(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_answer = message.text
    await add_user_facts(user_id, 'style of communication', user_answer)
    await message_in_user_lang(message, user_id, 'done with questions')
    await state.clear()

#classes for reminders
class UserSettings(StatesGroup):
    water_reminder = State()
    food_reminder = State()
    sleep_reminder = State()



# commands
@user.message(Command('water'))
async def water(message: types.Message):
    user_id = message.from_user.id
    if await get_user_facts(user_id, 'water_reminder')=='ON':
        await add_reminder(user_id, 'water_reminder', 'OFF')
        await message.answer(
            'got it! i will not remind you to drink water anymore'
        )
    else:
        await add_reminder(user_id, 'water_reminder', 'ON')
        await message.answer(
        'got it! now i will remind you to drink water ;)'
        )

@user.message(Command('sleep'))
async def sleep(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await get_user_facts(user_id, 'sleep_reminder') == 'ON':
        await add_reminder(user_id, 'sleep_reminder', 'OFF')
        await message.answer(
            'got it! i will not remind you to go to sleep anymore'
        )
    else:
        await add_reminder(user_id, 'sleep_reminder', 'ON')
        await message.answer(
            'got it! now i will remind you to go to sleep ;)'
        )

@user.message(Command('food'))
async def food(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if await get_user_facts(user_id, 'food_reminder') == 'ON':
        await add_reminder(user_id, 'food_reminder', 'OFF')
        await message.answer(
            'got it! i will not remind you to eat anymore'
        )
    else:
        await add_reminder(user_id, 'food_reminder', 'ON')
        await message.answer(
            'got it! now i will remind you to eat ;)'
        )


#callbacks
@user.callback_query(F.data=='not_work')
async def why(callback: CallbackQuery):
    await callback.message.answer('Why?', reply_markup=kb.options)
    await callback.answer()

@user.callback_query(F.data=='work')
async def mb_timer(callback: CallbackQuery):
    await callback.message.answer('great! do i start the timer?', reply_markup=kb.start_timer)
    await callback.answer()

@user.callback_query(F.data=='start_timer')
async def start_timer(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.answer('start it is!', reply_markup=kb.options_timer)
    user_focus_time[user_id] = time.time()
    await callback.answer()



#timer
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
    time_of_start = user_focus_time.get(user_id)
    if time_of_start:
        total_seconds = time.time() - time_of_start
        delta = timedelta(seconds=total_seconds)
        today = datetime.now().strftime('%Y-%m-%d')
        user_id = callback.from_user.id
        await callback.message.answer(f"you've been focused for {format_seconds(total_seconds)}!")
        await add_focus_time(user_id, today, delta)

@user.message(Command('TotalFocus'))
async def total_focus(message: types.Message):
    user_id = message.from_user.id
    today = datetime.now().strftime('%Y-%m-%d')
    focus_time = await get_user_time(user_id, today)
    if focus_time:
        await message.answer(f"Today you've been focused for {focus_time}!")
    else:
        await message.answer("You haven't focused today yet!")
