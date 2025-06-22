from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

base64_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔐 Encode", callback_data="base64:encode"),
            InlineKeyboardButton(text="🔓 Decode", callback_data="base64:decode"),
        ]
    ])