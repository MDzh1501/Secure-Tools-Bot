from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello, world!")

