from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


async def create_markup(**kwargs) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in kwargs
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


home_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подготовка', callback_data='prepare'),
     InlineKeyboardButton(text='Отметить детей', callback_data='marking')],
    [InlineKeyboardButton(text='Обновление', callback_data='new_day')],
    [InlineKeyboardButton(text='Список детей', callback_data='pool')]
])


back_home_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='home')]
], resize_keyboard=True)


profile_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='удалить', callback_data='delete_profile'),
     InlineKeyboardButton(text='change', callback_data='edit_profile')]
])

back_pool_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='pool'), KeyboardButton(text='home')]
], resize_keyboard=True)