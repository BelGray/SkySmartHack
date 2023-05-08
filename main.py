import sqlite3
from skysmart.skysmart_api import SkySmartApi
from secret import token
from aiogram import executor, types
from skysmarthack.loader import dp
from skysmarthack.bot_commands import set_default_commands
import aiogram

#в переменной token находится токен от вашего аккаунта в SkySmart


SSApi = SkySmartApi(token)

#Подключение к базе данных
bot_db = sqlite3.connect("bot.db")
cursor = bot_db.cursor()

#Подключение к боту Telegram
async def on_startup(dispatcher):
    print("БОТ ПОДКЛЮЧЕН К TELEGRAM API УСПЕШНО!")
    await set_default_commands(dispatcher)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Отвечу на любой тест уже скоро!")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
