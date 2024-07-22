from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from data.config import parol
from keyboards.default.admin_buttons import admin_btn
from keyboards.inline.inline_buttons import *


@dp.message_handler(commands='start')
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu Aleykum, <b>{message.from_user.full_name}</b>!", reply_markup=menyu_button)


from utils.db_api.sql_database import *
from states.crm_states import All_States


@dp.message_handler(commands='register')
async def registratin(message: types.Message):
    data = check_user(user_id=message.from_user.id)
    if data is None:
        await message.answer('Ro`yxatdan o`tish uchun ismingizni kiriting !')
        await All_States.ism_kiritish.set()
    else:
        await message.answer('Siz oldin ro`yxatdan o`tgansiz')


@dp.message_handler(state=All_States.ism_kiritish, content_types=types.ContentType.TEXT)
async def kabinet_ism(message: types.Message, state: FSMContext):
    full_name = message.text
    data = register_user(user_id=message.from_user.id, full_name=full_name)
    await message.answer(data)
    await state.finish()


@dp.message_handler(commands='edit_name')
async def name_editor(message: types.Message):
    await message.answer('Yangi ism kiriting')
    await All_States.ism_ozgartirish.set()


@dp.message_handler(state=All_States.ism_ozgartirish, content_types=types.ContentType.TEXT)
async def kabinet_ism_ozgartirish(message: types.Message, state: FSMContext):
    full_name = message.text
    data = change_name(user_id=message.from_user.id, full_name=full_name)
    await message.answer(data)
    await state.finish()


@dp.message_handler(commands='admin')
async def admin_panel(message: types.Message):
    await message.answer('Parolni kiriting')
    await All_States.password_state.set()


@dp.message_handler(state=All_States.password_state)
async def admin_uchun(message: types.Message):
    if message.text == parol:
        await message.answer('Siz admin paneldasiz!', reply_markup=admin_btn)
        await All_States.admin.set()
    else:
        await message.answer('Parol xato')


@dp.message_handler(text='Xodimlar ro`yxati !', state=All_States.admin)
async def name_uchun(message: types.Message, state: FSMContext):
    userlar = list_users()
    print(userlar)
    txt = ''
    for user_id, user_name in userlar:
        txt += f"🧍<a href='tg://user?id={user_id}'>{user_name}</a>\n\n"
    await message.answer(txt, parse_mode='HTML')


@dp.message_handler(text='Vazifa yuklash !', state=All_States.admin)
async def vazifa_ismlar(message: types.Message):
    userlar = list_users()
    print(userlar)

    odamlar_button = types.InlineKeyboardMarkup()
    for i in userlar:
        odamlar_button.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
    await message.answer('Xodimlardan birini tanlang 😊', reply_markup=odamlar_button)
    await All_States.vazifa_yuklash.set()


from loader import bot


@dp.callback_query_handler(state=All_States.vazifa_yuklash)
async def tasdiqlash(call: types.CallbackQuery,state:FSMContext):
    user_id_task = call.data
    await call.message.answer('Vazifani kiriting 😊')
    await All_States.vazifa_text.set()

    @dp.message_handler(state=All_States.vazifa_text)
    async def tasdiqlama(message: types.Message):
        add_Task(user_id=str(user_id_task), task_text=message.text, date_task=message.date)

        await bot.send_message(user_id_task,
                               text=f"{message.text}\n\n Sizga <b>{message.from_user.full_name}</b> tomonidan yuklatildi")
        await message.answer('Vazifa xodimga yuborildi')
        await All_States.admin.set()


@dp.message_handler(text='Xodimni o`chirish', state=All_States.admin)
async def delete_user(message: types.Message):
    userlar = list_users()
    print(userlar)

    odamlar_button = types.InlineKeyboardMarkup()
    for i in userlar:
        odamlar_button.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
    await message.answer('Xodimlardan birini tanlang', reply_markup=odamlar_button)
    await All_States.ochirish.set()


import asyncio


@dp.callback_query_handler(state=All_States.ochirish)
async def delete_state(call: types.CallbackQuery):
    name = delete_user_id(int(call.data))
    print(call.data)
    print(type(call.data))
    print(name)
    await call.answer(f'{name[0]} O`chirildi')

    userlar = list_users()
    print(userlar)

    odamlar_button = types.InlineKeyboardMarkup()
    for i in userlar:
        odamlar_button.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))

    await call.message.edit_reply_markup(reply_markup=odamlar_button)
    await asyncio.sleep(5)
    await call.message.delete()
    await All_States.admin.set()


@dp.callback_query_handler(text="tasks")
async def all_tasks(call: types.CallbackQuery):
    list_tasks = User_task(user_id=str(call.message.chat.id))
    print(list_tasks)
    tt = []
    if list_tasks != tt:
        await call.message.answer('Sizning vazifalaringiz')
        
        tayyor_text = ''
        print(list_tasks)
        for i in range(len(list_tasks)):
            for d in range(len(list_tasks[i])):
                if d == 0:
                    tayyor_text += '📃' + list_tasks[i][d] + '\n'
                elif d == 1:
                    tayyor_text += '🆔' + list_tasks[i][d] + '\n'
                elif d == 2:
                    tayyor_text += '⏳' + list_tasks[i][d] + '\n'
                elif d == 3:
                    if list_tasks[i][d] == 'bajarilmadi':
                        tayyor_text += '❌' + list_tasks[i][d] + '\n\n'
                    else:
                        tayyor_text += '✅' + list_tasks[i][d] + '\n\n'

            tayyor_text += '------------------\n\n'
        await call.message.answer(tayyor_text)
    else:
        await call.message.answer('Sizga vazifa yuklatilmagan😒')


@dp.callback_query_handler(text='sucses')
async def ajwhdvajwd(call:types.CallbackQuery):
    list_tasks=sucsess_task(user_id=str(call.message.chat.id))
    print(list_tasks)
    tt = []
    if list_tasks == tt:
        await call.message.answer('Sizda Bajarilgan Vazifa yoq 🤦‍♂️')
    else:
        tayyor_text = ''
        for i in range(len(list_tasks)):
            for d in range(len(list_tasks[i])):
                if d == 0:
                    tayyor_text += '📃' + list_tasks[i][d] + '\n'
                elif d == 1:
                    tayyor_text += '🆔' + list_tasks[i][d] + '\n'
                elif d == 2:
                    tayyor_text += '⏳' + list_tasks[i][d] + '\n'
                elif d == 3:
                    if list_tasks[i][d] == 'bajarilmadi':
                        tayyor_text += '❌' + list_tasks[i][d] + '\n\n'
                    else:
                        tayyor_text += '✅' + list_tasks[i][d] + '\n\n'

            tayyor_text += '------------------\n\n'
        await call.message.answer(tayyor_text)


@dp.callback_query_handler(text='not_sucses')
async def ajwhdvajwd(call:types.CallbackQuery):
    list_tasks=notsucsess_task(user_id=str(call.message.chat.id))
    print(list_tasks)
    tt = []
    if list_tasks == tt:
        await call.message.answer('Sizda Bajarilmagan Vazifa yoq 😊')
    else:
        tayyor_text = ''
        for i in range(len(list_tasks)):
            for d in range(len(list_tasks[i])):
                if d == 0:
                    tayyor_text += '📃' + list_tasks[i][d] + '\n'
                elif d == 1:
                    tayyor_text += '🆔' + list_tasks[i][d] + '\n'
                elif d == 2:
                    tayyor_text += '⏳' + list_tasks[i][d] + '\n'
                elif d == 3:
                    if list_tasks[i][d] == 'bajarilmadi':
                        tayyor_text += '❌' + list_tasks[i][d] + '\n\n'
                    else:
                        tayyor_text += '✅' + list_tasks[i][d] + '\n\n'

            tayyor_text += '------------------\n\n'
        await call.message.answer(tayyor_text)


@dp.message_handler(text='Vazifani Tugatish⏱',state='*')
async def vazifa(message:types.Message):
    userlar = list_users()
    print(userlar)

    odamlar_button = types.InlineKeyboardMarkup()
    for i in userlar:
        odamlar_button.add(types.InlineKeyboardButton(text=i[1], callback_data=i[0]))
    await message.answer('Xodimlardan birini tanlang', reply_markup=odamlar_button)
    await All_States.filtr_id.set()
@dp.callback_query_handler(state=All_States.filtr_id)
async def vazifa_id(call:types.CallbackQuery,state:FSMContext):
    user_idsi = call.data
    list_tasks=notsucsess_task(user_id=str(call.data))
    print(list_tasks)
    tt = []
    if list_tasks == tt:
        await call.message.answer('Sizda Bajarilmagan Vazifa yoq 😊')
    else:
        count = 0
        tayyor_text = ''
        for i in range(len(list_tasks)):

            for d in range(len(list_tasks[i])):
                if d == 0:
                    tayyor_text += '📃' + list_tasks[i][d] + '\n'
                elif d == 1:
                    tayyor_text += '🆔' + list_tasks[i][d] + '\n'
                elif d == 2:
                    tayyor_text += '⏳' + list_tasks[i][d] + '\n'
                elif d == 3:
                    if list_tasks[i][d] == 'bajarilmadi':
                        count+=1
                        tayyor_text += f'🔢{count}\n❌' + list_tasks[i][d] + '\n\n'
                    else:
                        tayyor_text += '✅' + list_tasks[i][d] + '\n\n'

            tayyor_text += '------------------\n\n'
        await call.message.answer(tayyor_text)
        await call.message.answer('Qaysi vazifani yakunlamoqchisiz 🔢 kiriting')
        await All_States.id_tanlash.set()

    @dp.message_handler(state=All_States.id_tanlash)
    async def id_tanla(message:types.Message):
        if message.text.isdigit():
            soni  = int(message.text)-1
            list_tasks=notsucsess_task(user_id=str(user_idsi))
            keyboard_iline = types.InlineKeyboardMarkup()
            keyboard_iline.add(types.InlineKeyboardButton(text='Tugatish ⏱',callback_data=list_tasks[soni][0]))

            await message.answer(f"📃 {list_tasks[soni][0]}",reply_markup=keyboard_iline)
            await All_States.rating.set()
@dp.callback_query_handler(state=All_States.rating)
async def caller(call:types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=star_button)
    await All_States.star_result.set()

    @dp.callback_query_handler(state=All_States.star_result)
    async def star(call:types.CallbackQuery):
        soni = int(call.data)
        '''⭐️'''
        stars_dict = {
            '1':' ',
            '2':' ',
            '3':' ',
            '4':' ',
            '5':' ',
        }
        for i in range(soni):
            stars_dict[str(i+1)] = '''⭐️'''



        star_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{stars_dict['1']}",callback_data='1'),
                InlineKeyboardButton(text=f"{stars_dict['2']}",callback_data='2'),
                InlineKeyboardButton(text=f"{stars_dict['3']}",callback_data='3'),
                InlineKeyboardButton(text=f"{stars_dict['4']}",callback_data='4'),
                InlineKeyboardButton(text=f"{stars_dict['5']}",callback_data='5'),
                    ]
                    
                ]
            )
        star_button.add(
            types.InlineKeyboardButton(text='Tasdiqlash ✅',callback_data=f'{soni}')
            )

        await call.message.edit_reply_markup(reply_markup=star_button)
        # @dp.message_handler(text='Tasdiqlash ✅',state=All_States.star_result)


    # await call.message.answer(call.data)
    # await state.finish()
