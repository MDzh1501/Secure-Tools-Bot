from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


base64_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔐 Кодувати", callback_data="base64:encode"),
            InlineKeyboardButton(text="🔓 Розшифрувати", callback_data="base64:decode")
        ]
    ])

uuid_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="🔢 v1 - З мітки часу та MAC-адреси (не є безпечним)",
            callback_data="uuid:1"
        )
    ],
    [
        InlineKeyboardButton(
            text="🧠 v3 - Простір імен + ім'я (MD5, детермінований)",
            callback_data="uuid:2"
        )
    ],
    [
        InlineKeyboardButton(
            text="🎲 v4 - Повністю випадковий UUID (безпечний)",
            callback_data="uuid:3"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔐 v5 - Простір імен + ім'я (SHA-1, детермінований)",
            callback_data="uuid:4"
        )
    ],
    [
        InlineKeyboardButton(
            text="🧬 З hex - 32-х символьний рядок UUID",
            callback_data="uuid:5"
        )
    ]
])

hashing_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показати доступні способи хешування", callback_data="hash:guaranteed")
    ]
])

url_choice_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔐 Кодувати", callback_data="url:encode"),
        InlineKeyboardButton(text="🔓 Розшифрувати", callback_data="url:decode")
    ]
])

url_encoding_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🔠 Вибрати тип кодування", callback_data="url:encoding")
    ],
    [
        InlineKeyboardButton(text="➕ Змінити пробіли на \"+\"", callback_data="url:plus_included")
    ],
    [
        InlineKeyboardButton(text="❌ Ввести символи, які не треба кодувати в url формат", callback_data="url:safe")
    ],
    [
        InlineKeyboardButton(text="✅ Перейти далі", callback_data="url:proceed_encode")
    ]
])

skip_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Пропустити")], ], resize_keyboard=True, one_time_keyboard=True
)