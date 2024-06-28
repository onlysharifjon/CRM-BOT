from aiogram.dispatcher.filters.state import StatesGroup, State


class All_States(StatesGroup):
    ism_kiritish = State()
    ism_ozgartirish = State()
    password_state = State()
    admin = State()
    vazifa_yuklash = State()
    vazifa_text = State()
    ochirish = State()
