from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from data.config import parol
from keyboards.default.admin_buttons import admin_btn


@dp.message_handler(commands='start')
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu Aleykum, <b>{message.from_user.full_name}</b>!")


