from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = ""

bot = Bot(TOKEN)
dp = Dispatcher()