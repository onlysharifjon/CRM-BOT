from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

# odamlar = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(),
#             InlineKeyboardButton
#         ]
#     ]
# )

menyu_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Vazifalar 📃', callback_data='tasks')
        ],
        [
            InlineKeyboardButton('Bajarilganlar 📃', callback_data='sucses')
        ],
        [
            InlineKeyboardButton('Bajarilmaganlar 📃', callback_data='not_sucses')
        ],
        [
            InlineKeyboardButton('Rating ⭐️', callback_data='rating')
        ]
    ]
)