from loader import dp
from aiogram import types


@dp.message_handler(commands='menu')
async def menu_sender(message: types.Message):
    await message.answer('Menyulardan birini tanlang')
