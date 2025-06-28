from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


base64_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔐 Encode", callback_data="base64:encode"),
            InlineKeyboardButton(text="🔓 Decode", callback_data="base64:decode"),
        ]
    ])

uuid_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="🔢 v1 — From timestamp & MAC (not privacy-safe)",
            callback_data="uuid:1"
        )
    ],
    [
        InlineKeyboardButton(
            text="🧠 v3 — Namespace + name (MD5, deterministic)",
            callback_data="uuid:2"
        )
    ],
    [
        InlineKeyboardButton(
            text="🎲 v4 — Fully random UUID (secure)",
            callback_data="uuid:3"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔐 v5 — Namespace + name (SHA-1, deterministic)",
            callback_data="uuid:4"
        )
    ],
    [
        InlineKeyboardButton(
            text="🧬 From hex — 32-char UUID string",
            callback_data="uuid:5"
        )
    ]
])

hashing_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показати доступні способи хешування", callback_data="hash:guaranteed")
    ]
])

