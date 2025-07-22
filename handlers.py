from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboard import *
from tools.base64_enc_dec import base64_encode, base64_decode
from tools.uuid_hash import *
from tools.hash_tool import *
from tools.url_service import url_encode, url_decode



router = Router()

# === FSM States ===
class StartState(StatesGroup):
    active = State()


class Base64State(StatesGroup):
    encode_input = State()
    decode_input = State()
    encoding_type = State()


class UUIDState(StatesGroup):
    choosing_type = State()
    entering_name = State()
    entering_hex = State()


class HashStates(StatesGroup):
    choosing_algo = State()
    waiting_info = State()


class URLStates(StatesGroup):
    input_text = State()
    choosing_encoding = State()
    safe_features = State()


# === Handlers ===
def requires_started():
    def decorator(handler):
        async def wrapper(*args, **kwargs):
            # Try to find FSMContext and Message in args or kwargs
            state = kwargs.get('state')
            message = kwargs.get('message')

            # If not found in kwargs, try to find in args by type
            if state is None or message is None:
                for arg in args:
                    if isinstance(arg, FSMContext):
                        state = arg
                    elif isinstance(arg, Message):
                        message = arg

            if state is None or message is None:
                return await handler(*args, **kwargs)

            data = await state.get_data()
            if not data.get("started"):
                await message.answer("❗ Please use /start before using commands.")
                return

            return await handler(*args, **kwargs)
        return wrapper
    return decorator


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    await state.update_data(started=True)  # <-- set flag in data, not state
    await message.answer("🤖 Привіт, ласкаво просимо до Security Tools Bot!")

# -=-=- Command handlers -=-=-
@router.message(Command('base64'))
@requires_started()
async def base64_start(message: Message, state: FSMContext, **kwargs):
    await message.answer("Виберіть варіант:", reply_markup=base64_keyboard)


@router.message(Command('uuid'))
@requires_started()
async def uuid_start(message: Message, state: FSMContext, **kwargs):
    await message.answer("Як згенерувати UUID?", reply_markup=uuid_keyboard)


@router.message(Command('hash'))
@requires_started()
async def hash_start(message: Message, state: FSMContext, **kwargs):
    await message.answer("Оберіть алгоритм хешування (наприклад, sha256)", reply_markup=hashing_keyboard)
    await state.set_state(HashStates.choosing_algo)


@router.message(Command('url'))
@requires_started()
async def url_start(message: Message, state: FSMContext, **kwargs):
    await message.answer("Оберіть вашу дію:", reply_markup=url_choice_keyboard)


# -=-=- Query and FSM context handlers -=-=-
@router.callback_query(F.data.startswith("base64:"))
async def base64_callback(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]

    await state.update_data(action=action)

    await callback.message.answer("По-перше, яке кодування ви хочете використовувати? (наприклад, utf-8, ascii)")
    await state.set_state(Base64State.encoding_type)

    await callback.answer()


@router.message(Base64State.encoding_type)
async def receive_encoding_type(message: Message, state: FSMContext):
    encoding = message.text.strip().lower()
    data = await state.get_data()
    action = data.get("action")

    await state.update_data(encoding=encoding)

    if action == "encode":
        await message.answer("Тепер надішліть текст, який ви хочете закодувати.")
        await state.set_state(Base64State.encode_input)
    elif action == "decode":
        await message.answer("Тепер надішліть рядок Base64, який ви хочете декодувати.")
        await state.set_state(Base64State.decode_input)


@router.message(Base64State.encode_input)
async def handle_encoding(message: Message, state: FSMContext):
    data = await state.get_data()
    encoding = data.get("encoding", "utf-8")
    result = base64_encode(message.text, encoding)
    await message.answer("Результат: ")
    await message.answer(f"{result}", parse_mode="Markdown")
    await state.set_state(None)


@router.message(Base64State.decode_input)
async def handle_decoding(message: Message, state: FSMContext):
    data = await state.get_data()
    encoding = data.get("encoding", "utf-8")
    result = base64_decode(message.text, encoding)
    await message.answer("Результат: ")
    await message.answer(f"{result}", parse_mode="Markdown")
    await state.set_state(None)


@router.callback_query(F.data.startswith("uuid:"))
async def uuid_choose(callback: CallbackQuery, state: FSMContext):
    version = callback.data.split(":")[1]
    await state.set_data({"version": version})
    
    if version == "1" or version == "3":
        result = hash_info_uuid("uuid:" + version)
        await callback.message.answer(f"UUID v{version}: `{result}`", parse_mode="Markdown")
        await state.set_state(None)
    
    elif version == "2" or version == "4":
        await callback.message.answer("Введіть *ім'я* для генерації UUID:", parse_mode="Markdown")
        await state.set_state(UUIDState.entering_name)
    
    elif version == "5":
        await callback.message.answer("Введіть 32-х символьний шістнадцятковий рядок:", parse_mode="Markdown")
        await state.set_state(UUIDState.entering_hex)
    
    await callback.answer()


@router.message(UUIDState.entering_name)
async def handle_name_input(message: Message, state: FSMContext):
    data = await state.get_data()
    version = data.get("version")
    name = message.text.strip()

    namespace = uuid.NAMESPACE_DNS  

    result = hash_info_uuid(f"uuid:{version}", namespace=namespace, name=name)
    await message.answer(f"✅ Дізнався твоє ім'я. UUID v{version} результат:\n`{result}`", parse_mode="Markdown")
    await state.set_state(None)


@router.message(UUIDState.entering_hex)
async def handle_hex_input(message: Message, state: FSMContext):
    hex_str = message.text.strip()
    result = hash_info_uuid("uuid:5", hex=hex_str)
    await message.answer(f"✅ Використовуючи ваш шістнадцятковий ввід. UUID з шістнадцяткової системи числення:\n`{result}`", parse_mode="Markdown")
    await state.set_state(None)


@router.callback_query(F.data == "hash:guaranteed")
async def show_hash_algorithms(callback: CallbackQuery):
    text = get_supported_hashes()
    await callback.message.edit_text(text, parse_mode="Markdown")
    await callback.answer()


@router.message(HashStates.choosing_algo)
async def choose_algo(message: Message, state: FSMContext):
    algo = message.text.strip().lower()

    if algo not in hashlib.algorithms_guaranteed:
        await message.answer(f"❌ Алгоритм \"{algo}\" не підтримується.\nНадішліть один з доступних.")
        return

    await state.update_data(chosen_algo=algo)
    await message.answer("Тепер надішліть текст, файл або фото для хешування")
    await state.set_state(HashStates.waiting_info)


@router.message(HashStates.waiting_info, F.text)
async def handle_hash_text(message: Message, state: FSMContext):
    data = await state.get_data()
    algo = data.get("chosen_algo", "sha256")

    result = hash_text_info(algo, message.text)
    await message.answer(result)
    await state.set_state(None)


@router.message(HashStates.waiting_info, F.document)
@router.message(HashStates.waiting_info, F.photo)
async def handle_file_photo(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    algo = data.get("chosen_algo", "sha256")

    if message.photo:
        file = message.photo[-1]
    else:
        file = message.document

    file_info = await bot.get_file(file.file_id)
    file_path = f"/tmp/{file.file_unique_id}"

    await bot.download_file(file_info.file_path, destination=file_path)

    result = hash_file(file_path, algo)

    await message.answer(result)
    await state.set_state(None)


@router.callback_query(F.data.in_({"url:encode", "url:decode"}))
async def handle_url_action_start(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]
    await state.update_data(action=action, plus_included=False, safety="", encoding=None, text=None)
    await callback.message.answer("Надішліть ваш текст (повинен бути звичайним, байтовим чи вже зашифрованим)")
    await state.set_state(URLStates.input_text)
    await callback.answer()


@router.message(URLStates.input_text)
async def handle_url_input_text(message: Message, state: FSMContext):
    data = await state.get_data()
    action = data.get("action")
    text = message.text.strip()

    await state.update_data(text=text)

    if action == "encode":
        await message.answer("✅ Текст був отриман! Що хочете зробити далі? ", reply_markup=url_encoding_keyboard)
        await state.set_state(None)
    elif action == "decode":
        await message.answer("✏️ Тепер введіть тип кодування (наприклад, utf-8, ascii):")
        await state.set_state(URLStates.choosing_encoding)


@router.callback_query(F.data == "url:encoding")
async def handle_url_enc_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")

    if not isinstance(text, str):
        await callback.message.answer("❗ Неможливо обрати тип кодування — ваш ввід не є текстовим рядком.")
        await callback.answer()
        return

    await callback.message.answer("✏️ Введіть тип кодування (наприклад, utf-8, ascii, cp1251):")
    await state.set_state(URLStates.choosing_encoding)

    await callback.answer()


@router.message(URLStates.choosing_encoding)
async def handle_typed_encoding(message: Message, state: FSMContext):
    data = await state.get_data()
    action = data.get("action")
    text = data.get("text")
    encoding = message.text.strip().lower()

    # Перевірка валідності кодування
    try:
        ''.encode(encoding)
    except LookupError:
        await message.answer("❌ Тип кодування не підтримується. Спробуйте інший (наприклад, utf-8 або ascii).")
        return

    await state.update_data(encoding=encoding)

    if action == "encode":
        await message.answer(
            "✅ Тип кодування збережено. Що робити далі?",
            reply_markup=url_encoding_keyboard
        )
        await state.set_state(None)  # Якщо хочеш вийти зі стану, або на твій розсуд
    elif action == "decode":
        result = url_decode(text, encoding)
        await message.answer(f"🔐 Результат: {result}")
        await state.set_state(None)


@router.callback_query(F.data == "url:plus_included")
async def include_plus(callback: CallbackQuery, state: FSMContext):
    __plus_included = True
    await state.update_data(plus_included=__plus_included)
    await callback.message.answer("✅ Буде заміна пробілів на +! Що далі? ", reply_markup=url_encoding_keyboard)
    await callback.answer()


@router.callback_query(F.data == "url:safe")
async def include_safety_features(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введіть символи, які не будуть закодовані: ")
    await state.set_state(URLStates.safe_features)
    await callback.answer()


@router.message(URLStates.safe_features)
async def handle_safety_features(message: Message, state: FSMContext):
    safety_input = message.text.strip()
    safety = safety_input.replace(" ", '')

    await state.update_data(safety=safety)
    await message.answer("✅ Символи збережено! Що далі?", reply_markup=url_encoding_keyboard)
    await state.set_state(None)  # Або залишай, якщо хочеш чекати наступні дії


@router.callback_query(F.data == "url:proceed_encode")
async def proceed_url_encoding(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    encoding = data.get("encoding", "utf-8")
    safety = data.get("safety", "")
    plus_included = data.get("plus_included", False)

    if not isinstance(text, str):
        await callback.message.answer("❌ Текст має бути рядком. Спробуйте ще раз.")
        await callback.answer()
        return

    try:
        result = url_encode(
            text=text,
            encoding=encoding,
            safety_features=safety,
            parse_plus=plus_included
        )
        await callback.message.answer(f"🔐 Результат кодування:\n`{result}`", parse_mode="Markdown")
    except Exception as e:
        await callback.message.answer(f"❌ Помилка при кодуванні:\n{str(e)}")

    await state.set_state(None)
    await state.update_data(plus_included=False, safety="", encoding=None, text=None, action=None)
    await callback.answer()


@router.message()
async def fallback(message: Message, state: FSMContext):
    if message.text and message.text.startswith("/"):
        return

    data = await state.get_data()
    if not data.get("started"):
        return

    await message.answer("Вибачте, я не зрозумів цього. Спробуй команду.")