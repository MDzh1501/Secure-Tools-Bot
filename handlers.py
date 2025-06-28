from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboard import base64_keyboard, uuid_keyboard
from base64_enc_dec import base64_encode, base64_decode
from uuid_hash import *



router = Router()


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


def requires_started():
    def decorator(handler):
        async def wrapper(message: Message, state: FSMContext, *args, **_):
            data = await state.get_data()
            if not data.get("started"):
                await message.answer("❗ Please use /start before using commands.")
                return
            return await handler(message, state, *args)
        return wrapper
    return decorator


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(started=True)
    await message.answer("🤖 Hello, welcome to the Security Tools Bot!")


@router.message(Command('base64'))
@requires_started()
async def base64_things(message: Message, state: FSMContext):
    await message.answer("Choose an option:", reply_markup=base64_keyboard)


@router.message(Command('uuid'))
@requires_started()
async def uuid_things(message: Message, state: FSMContext):
    await message.answer("How do you want to generate an UUID?", reply_markup=uuid_keyboard)


@router.callback_query(F.data.startswith("base64:"))
async def base64_callback(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]

    await state.set_data({"action": action})

    await callback.message.answer("Firstly, what encoding do you want to use? (e.g. utf-8, ascii)")
    await state.set_state(Base64State.encoding_type)

    await callback.answer()


@router.message(Base64State.encoding_type)
async def receive_encoding_type(message: Message, state: FSMContext):
    encoding = message.text.strip().lower()
    data = await state.get_data()
    action = data.get("action")

    await state.update_data(encoding=encoding)

    if action == "encode":
        await message.answer("Now send the text you want to encode.")
        await state.set_state(Base64State.encode_input)
    elif action == "decode":
        await message.answer("Now send the Base64 string you want to decode.")
        await state.set_state(Base64State.decode_input)


@router.message(Base64State.encode_input)
async def handle_encoding(message: Message, state: FSMContext):
    data = await state.get_data()
    encoding = data.get("encoding", "utf-8")
    result = base64_encode(message.text, encoding)
    await message.answer("Result: ")
    await message.answer(f"{result}", parse_mode="Markdown")
    await state.set_state(None)


@router.message(Base64State.decode_input)
async def handle_decoding(message: Message, state: FSMContext):
    data = await state.get_data()
    encoding = data.get("encoding", "utf-8")
    result = base64_decode(message.text, encoding)
    await message.answer("Result: ")
    await message.answer(f"{result}", parse_mode="Markdown")
    await state.set_state(None)


@router.callback_query(F.data.startswith("uuid:"))
async def uuid_choose(callback: CallbackQuery, state: FSMContext):
    version = callback.data.split(":")[1]
    await state.set_data({"version": version})
    
    if version == "1" or version == "3":
        result = hash_info_uuid("uuid:" + version)
        await callback.message.answer(f"UUID v{version}: `{result}`", parse_mode="Markdown")
        await state.clear()
    
    elif version == "2" or version == "4":
        await callback.message.answer("Enter a *name* for UUID generation:", parse_mode="Markdown")
        await state.set_state(UUIDState.entering_name)
    
    elif version == "5":
        await callback.message.answer("Enter a 32-char hex string:", parse_mode="Markdown")
        await state.set_state(UUIDState.entering_hex)
    
    await callback.answer()


@router.message(UUIDState.entering_name)
async def handle_name_input(message: Message, state: FSMContext):
    data = await state.get_data()
    version = data.get("version")
    name = message.text.strip()

    namespace = uuid.NAMESPACE_DNS  

    result = hash_info_uuid(f"uuid:{version}", namespace=namespace, name=name)
    await message.answer(f"✅ Got your name. UUID v{version} result:\n`{result}`", parse_mode="Markdown")
    await state.clear()


@router.message(UUIDState.entering_hex)
async def handle_hex_input(message: Message, state: FSMContext):
    hex_str = message.text.strip()
    result = hash_info_uuid("uuid:5", hex=hex_str)
    await message.answer(f"✅ Using your hex input. UUID from hex:\n`{result}`", parse_mode="Markdown")
    await state.clear()


@router.message()
async def fallback(message: Message, state: FSMContext):
    if message.text and message.text.startswith("/"):
        return

    current_state = await state.get_state()
    if current_state != StartState.active:
        return

    await message.answer("Sorry, I didn't understand that. Try a command.")
