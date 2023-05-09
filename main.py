import sqlite3
from systems import promocode
from database.sql_configs import cursor, bot_db
from skysmart.skysmart_api import SkySmartApi
from secret import skysmart_token
from aiogram import executor, types
from skysmarthack.loader import dp
from skysmarthack.bot_commands import set_default_commands

default_task_url = "edu.skysmart.ru/student/"
SSApi = SkySmartApi(skysmart_token)

#Подключение к Telegram API
async def on_startup(dispatcher):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id VARCHAR,
            premium INTEGER,
            premium_ends VARCHAR,
            available_answers INTEGER
    );""")
        bot_db.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            body VARCHAR,
            description VARCHAR,
            item_id INTEGER,
            usages INTEGER
            );""")
        bot_db.commit()

    except Exception as e:
        print(e)
    print("ПОДКЛЮЧЕНИЕ К TELEGRAM API СОВЕРШЕНО УСПЕШНО")
    await set_default_commands(dispatcher)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Отвечу на любой тест уже скоро!")

@dp.message_handler()
async def message_handler(message: types.Message):
    if default_task_url in message["text"]:
        pass

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
