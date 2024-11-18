from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from interface import *

async def create_markup(button: dict) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in button.items()
    ]
    print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


home_menu_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=prepare_btn),
     KeyboardButton(text=mark_children_btn)],
    [KeyboardButton(text=update_btn)],
    [KeyboardButton(text=children_list_btn)]
], resize_keyboard=True)

profile_menu_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=delete_btn, callback_data='delete_profile'),
     InlineKeyboardButton(text=change_btn, callback_data='edit_profile')],
    [InlineKeyboardButton(text=back_pool_btn, callback_data='pool')]
])