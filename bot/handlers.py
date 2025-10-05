from aiogram import types
from aiogram.filters import Command
from .bot import dp
import aiosqlite

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Hello")