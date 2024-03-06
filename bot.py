import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.send_message import SendMessage

import sqlite3
connection = sqlite3.connect('21meet.db')

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT = os.getenv("ADMIN_CHAT_ID")

dp = Dispatcher()
form_router = Router()
dp.include_router(form_router)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

class Form(StatesGroup):
    order = State()
    price = State()
    confirm = State()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [types.KeyboardButton(text='Сделать заказ')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", reply_markup=keyboard)

@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    kb = [
            [types.KeyboardButton(text='Сделать заказ')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


    await message.answer(
        "Действие отменено.",
        reply_markup=keyboard
    )




@form_router.message(F.text.lower() == 'сделать заказ')
async def place_order(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.order) 
    kb = [
            [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


    await message.answer("Отправь мне название позиции в меню", reply_markup=keyboard)
    

@form_router.message(Form.order)
async def process_order(message: Message, state: FSMContext):
    await state.update_data(order=message.text)
    await state.set_state(Form.price)
    kb = [
            [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


    await message.answer(f"Отправь мне цену данной позиции: {message.text}", reply_markup=keyboard)

@form_router.message(Form.price)
async def process_price(message: Message, state: FSMContext):
    data = await state.update_data(price=message.text)
    await state.set_state(Form.confirm)
    kb = [
        [types.KeyboardButton(text='Да')],
        [types.KeyboardButton(text='Нет')],
        [types.KeyboardButton(text='Отмена')]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Ты заказал {data['order']} на сумму {data['price']}, всё верно?", reply_markup=keyboard)

@form_router.message(Form.confirm)
async def confirm_order(message: Message, state: FSMContext):
    data = await state.update_data(confirm=message.text)
    kb = [
            [types.KeyboardButton(text='Отмена')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    if data['confirm'] == 'Да':
        kb = [
            [types.KeyboardButton(text='Сделать заказ')]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.answer("Отправляю твой заказ официанту, ожидайте.", reply_markup=keyboard)
        await bot.send_message(chat_id=ADMIN_CHAT, text=f"Заказ от пользователя @{message.from_user.username}:\n {data['order']} - {data['price']} руб.")
    else:
        kb = [
            [types.KeyboardButton(text='Сделать заказ')]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Ваш заказ был отменён.", reply_markup=keyboard)


async def main() -> None:
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
