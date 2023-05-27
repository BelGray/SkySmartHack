import sqlite3
import traceback

import secret
import systems.pay
from skysmarthack.logger import logAction
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import skysmarthack.buttons
from systems import promocode
from skysmarthack.keyboards import *
from systems.tool_methods import *
from skysmart.task_answer import TaskAnswerObject
from database.sql_configs import cursor, bot_db
from skysmart.skysmart_api import SkySmartApi
from secret import skysmart_token
from aiogram import executor, types
from skysmarthack.loader import dp, bot
from skysmarthack.bot_commands import set_default_commands, commands_list

SSApi = SkySmartApi(skysmart_token)
bills_lifetime = 5

class DeletePromo(StatesGroup):
    id = State()
class ActivatePromo(StatesGroup):
    promocode = State()
class NewPromo(StatesGroup):
    body = State()


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

@dp.message_handler(commands=['buy_answers'])
async def buy_answers(message: types.Message):
    await logAction(buy_answers, True, message)
    registered = userRegister(message.from_user.id)
    if registered:
        text = f"""💳 <b>Купить ответы на тесты</b>

📌 10 ответов - 30₽
📌 25 ответов - 70₽ [-7%]
📌 50 ответов - 130₽ [-14%]
📌 75 ответов - 180₽ [-20%]
📌 100 ответов - 225₽ [-25%]"""
        await message.answer(text, parse_mode="HTML", reply_markup=skysmarthack.buttons.BuyAnswersButtonClient)
    else:
        await message.answer("⭕ Что-то пошло не так! Повтори попытку позже!")

@dp.callback_query_handler(text="buy_100_answers")
async def buy_100_answers_callback(message: types.Message):
    await logAction(buy_100_answers_callback, True, message)
    qiwi = systems.pay.QiwiPayment(secret.qiwi_secret_data["api_belgray_key"])
    count = 100
    amount = 225
    lifetime = bills_lifetime
    chat_id = message["message"]["chat"]["id"]
    bill = await qiwi.buildBill(
        str(message.from_user.id),
        count = count,
        amount = amount,
        comment=f"{count} {'ответ(-а)' if count < 5 else 'ответов'} на тесты платформы SkySmart в телеграм-боте @skysmarthack_bot.\n\nTG-ID покупателя: {message.from_user.id}",
        bill_lifetime=lifetime
    )
    if bill[0]:
        PayBillButtonClient = InlineKeyboardMarkup(2)
        pay_bill_button = InlineKeyboardButton(text="🥝 Оплатить через QIWI", url=bill[1])
        PayBillButtonClient.insert(pay_bill_button)
        await bot.send_message(chat_id=chat_id, text=f"""💳 <b>Счет к оплате</b>

🎁 <b>Товар:</b> {count} ответов
💲 <b>Стоимость:</b> {amount}₽
🕓 <b>Время действия счета:</b> {lifetime} мин.
""", parse_mode="HTML", reply_markup=PayBillButtonClient)
        wait_for_pay = await qiwi.waitForPay(str(message.from_user.id), bill_id=bill[2], count=count)
        if wait_for_pay:
            await bot.send_message(chat_id=chat_id, text=f"✅ Оплата прошла успешно! На твой баланс зачислено <b>{count} {'ответ(-а)' if count < 5 else 'ответов'}</b>. Проверить - /profile", parse_mode="HTML")
        else:
            await bot.send_message(
                chat_id = chat_id,
                text=f"❌ Что-то пошло не так при оплате счета. Возможно, у него истек срок."
            )

    else:
        await message.answer("⭕ Что-то пошло не так при конструировании счета! Повтори попытку позже!")

@dp.callback_query_handler(text="buy_75_answers")
async def buy_75_answers_callback(message: types.Message):
    await logAction(buy_75_answers_callback, True, message)
    qiwi = systems.pay.QiwiPayment(secret.qiwi_secret_data["api_belgray_key"])
    count = 75
    amount = 180
    lifetime = bills_lifetime
    chat_id = message["message"]["chat"]["id"]
    bill = await qiwi.buildBill(
        str(message.from_user.id),
        count = count,
        amount = amount,
        comment=f"{count} {'ответ(-а)' if count < 5 else 'ответов'} на тесты платформы SkySmart в телеграм-боте @skysmarthack_bot.\n\nTG-ID покупателя: {message.from_user.id}",
        bill_lifetime=lifetime
    )
    if bill[0]:
        PayBillButtonClient = InlineKeyboardMarkup(2)
        pay_bill_button = InlineKeyboardButton(text="🥝 Оплатить через QIWI", url=bill[1])
        PayBillButtonClient.insert(pay_bill_button)
        await bot.send_message(chat_id=chat_id, text=f"""💳 <b>Счет к оплате</b>

🎁 <b>Товар:</b> {count} ответов
💲 <b>Стоимость:</b> {amount}₽
🕓 <b>Время действия счета:</b> {lifetime} мин.
""", parse_mode="HTML", reply_markup=PayBillButtonClient)
        wait_for_pay = await qiwi.waitForPay(str(message.from_user.id), bill_id=bill[2], count=count)
        if wait_for_pay:
            await bot.send_message(chat_id=chat_id, text=f"✅ Оплата прошла успешно! На твой баланс зачислено <b>{count} {'ответ(-а)' if count < 5 else 'ответов'}</b>. Проверить - /profile", parse_mode="HTML")
        else:
            await bot.send_message(
                chat_id = chat_id,
                text=f"❌ Что-то пошло не так при оплате счета. Возможно, у него истек срок."
            )

    else:
        await message.answer("⭕ Что-то пошло не так при конструировании счета! Повтори попытку позже!")


@dp.callback_query_handler(text="buy_50_answers")
async def buy_50_answers_callback(message: types.Message):
    await logAction(buy_50_answers_callback, True, message)
    qiwi = systems.pay.QiwiPayment(secret.qiwi_secret_data["api_belgray_key"])
    count = 50
    amount = 130
    lifetime = bills_lifetime
    chat_id = message["message"]["chat"]["id"]
    bill = await qiwi.buildBill(
        str(message.from_user.id),
        count = count,
        amount = amount,
        comment=f"{count} {'ответ(-а)' if count < 5 else 'ответов'} на тесты платформы SkySmart в телеграм-боте @skysmarthack_bot.\n\nTG-ID покупателя: {message.from_user.id}",
        bill_lifetime=lifetime
    )
    if bill[0]:
        PayBillButtonClient = InlineKeyboardMarkup(2)
        pay_bill_button = InlineKeyboardButton(text="🥝 Оплатить через QIWI", url=bill[1])
        PayBillButtonClient.insert(pay_bill_button)
        await bot.send_message(chat_id=chat_id, text=f"""💳 <b>Счет к оплате</b>

🎁 <b>Товар:</b> {count} ответов
💲 <b>Стоимость:</b> {amount}₽
🕓 <b>Время действия счета:</b> {lifetime} мин.
""", parse_mode="HTML", reply_markup=PayBillButtonClient)
        wait_for_pay = await qiwi.waitForPay(str(message.from_user.id), bill_id=bill[2], count=count)
        if wait_for_pay:
            await bot.send_message(chat_id=chat_id, text=f"✅ Оплата прошла успешно! На твой баланс зачислено <b>{count} {'ответ(-а)' if count < 5 else 'ответов'}</b>. Проверить - /profile", parse_mode="HTML")
        else:
            await bot.send_message(
                chat_id = chat_id,
                text=f"❌ Что-то пошло не так при оплате счета. Возможно, у него истек срок."
            )

    else:
        await message.answer("⭕ Что-то пошло не так при конструировании счета! Повтори попытку позже!")

@dp.callback_query_handler(text="buy_25_answers")
async def buy_25_answers_callback(message: types.Message):
    await logAction(buy_25_answers_callback, True, message)
    qiwi = systems.pay.QiwiPayment(secret.qiwi_secret_data["api_belgray_key"])
    count = 25
    amount = 70
    lifetime = bills_lifetime
    chat_id = message["message"]["chat"]["id"]
    bill = await qiwi.buildBill(
        str(message.from_user.id),
        count = count,
        amount = amount,
        comment=f"{count} {'ответ(-а)' if count < 5 else 'ответов'} на тесты платформы SkySmart в телеграм-боте @skysmarthack_bot.\n\nTG-ID покупателя: {message.from_user.id}",
        bill_lifetime=lifetime
    )
    if bill[0]:
        PayBillButtonClient = InlineKeyboardMarkup(2)
        pay_bill_button = InlineKeyboardButton(text="🥝 Оплатить через QIWI", url=bill[1])
        PayBillButtonClient.insert(pay_bill_button)
        await bot.send_message(chat_id=chat_id, text=f"""💳 <b>Счет к оплате</b>

🎁 <b>Товар:</b> {count} ответов
💲 <b>Стоимость:</b> {amount}₽
🕓 <b>Время действия счета:</b> {lifetime} мин.
""", parse_mode="HTML", reply_markup=PayBillButtonClient)
        wait_for_pay = await qiwi.waitForPay(str(message.from_user.id), bill_id=bill[2], count=count)
        if wait_for_pay:
            await bot.send_message(chat_id=chat_id, text=f"✅ Оплата прошла успешно! На твой баланс зачислено <b>{count} {'ответ(-а)' if count < 5 else 'ответов'}</b>. Проверить - /profile", parse_mode="HTML")
        else:
            await bot.send_message(
                chat_id = chat_id,
                text=f"❌ Что-то пошло не так при оплате счета. Возможно, у него истек срок."
            )

    else:
        await message.answer("⭕ Что-то пошло не так при конструировании счета! Повтори попытку позже!")

@dp.callback_query_handler(text="buy_10_answers")
async def buy_10_answers_callback(message: types.Message):
    await logAction(buy_10_answers_callback, True, message)
    qiwi = systems.pay.QiwiPayment(secret.qiwi_secret_data["api_belgray_key"])
    count = 10
    amount = 30
    lifetime = bills_lifetime
    chat_id = message["message"]["chat"]["id"]
    bill = await qiwi.buildBill(
        str(message.from_user.id),
        count = count,
        amount = amount,
        comment=f"{count} {'ответ(-а)' if count < 5 else 'ответов'} на тесты платформы SkySmart в телеграм-боте @skysmarthack_bot.\n\nTG-ID покупателя: {message.from_user.id}",
        bill_lifetime=lifetime
    )
    if bill[0]:
        PayBillButtonClient = InlineKeyboardMarkup(2)
        pay_bill_button = InlineKeyboardButton(text="🥝 Оплатить через QIWI", url=bill[1])
        PayBillButtonClient.insert(pay_bill_button)
        await bot.send_message(chat_id=chat_id, text=f"""💳 <b>Счет к оплате</b>

🎁 <b>Товар:</b> {count} ответов
💲 <b>Стоимость:</b> {amount}₽
🕓 <b>Время действия счета:</b> {lifetime} мин.
""", parse_mode="HTML", reply_markup=PayBillButtonClient)
        wait_for_pay = await qiwi.waitForPay(str(message.from_user.id), bill_id=bill[2], count=count)
        if wait_for_pay:
            await bot.send_message(chat_id=chat_id, text=f"✅ Оплата прошла успешно! На твой баланс зачислено <b>{count} {'ответ(-а)' if count < 5 else 'ответов'}</b>. Проверить - /profile", parse_mode="HTML")
        else:
            await bot.send_message(
                chat_id = chat_id,
                text=f"❌ Что-то пошло не так при оплате счета. Возможно, у него истек срок."
            )

    else:
        await message.answer("⭕ Что-то пошло не так при конструировании счета! Повтори попытку позже!")



@dp.message_handler(commands=["tools"])
async def tools(message: types.Message):
    await logAction(tools, True, message)
    registered = userRegister(message.from_user.id)
    is_trusted = isUserTrustedPerson(message.from_user.id)
    if registered:
        if is_trusted:
            await message.answer("""
⚙️ <b>Панель управления ботом</b>

Панель управления для разработчиков и доверенных пользователей.

Промокод: {id}-{body}-{item_id}
Создать новый промокод: {body}-{description}-{item_id}-{usages}
""", parse_mode="HTML", reply_markup=skysmarthack.buttons.ToolsMenuButtonClient)
        else:
            await message.answer("⭕ Команда доступна только разработчикам бота и доверенным пользователям!")
    else:
        await message.answer("⭕ Что-то пошло не так! Повтори попытку позже!")


@dp.message_handler(commands=["promo"])
async def promo(message: types.Message):
    await logAction(promo, True, message)
    registered = userRegister(message.from_user.id)
    if registered:
        await message.answer("🔑 Отлично! Теперь введи промокод")
        await ActivatePromo.promocode.set()
    else:
        await message.answer("❌ Что-то пошло не так при выполнении команды!")
@dp.message_handler(state=ActivatePromo.promocode)
async def process_promo_body(message: types.Message, state: FSMContext):
    await logAction(process_promo_body, True, message)
    await state.finish()
    full_promocode = message.text
    parts = full_promocode.split("-")
    if len(parts) == 3:
        promo_obj = promocode.AlreadyExistsPromo(full_promocode, message.from_user.id)
        promo_info = promo_obj.get_promo_info()
        if promo_info[0]:
            await message.answer(text=f"""🔑 <b>Промокод: |{full_promocode}|</b>

📝 Описание: {promo_info[1][2]}
🎁 Предмет: {promo_obj.item_ids[promo_info[1][3]]["available_answers"]} {"ответов" if promo_obj.item_ids[promo_info[1][3]]["available_answers"] > 4  else "ответ(-а)"}
☑️ Доступно активаций: {promo_info[1][4]}""", parse_mode="HTML", reply_markup=skysmarthack.buttons.ActivatePromoButtonClient)
        else:
            await message.answer("❌ Промокод не найден!")
    else:
        await message.answer("❌ Вид промокода не соответствует стандарту")

@dp.callback_query_handler(text="activate_promo_button")
async def activate_promo_callback(message: types.Message):
    await logAction(activate_promo_callback, True, message)
    text = message["message"]["text"]
    full_promo_splitting = text.split("|")
    full_promo = full_promo_splitting[1]
    promo_obj = promocode.AlreadyExistsPromo(full_promo, message["from"]["id"])
    promo_use = promo_obj.use_promo()
    if promo_use:
        await message.answer("✅ Промокод активирован успешно. Смотреть профиль - /profile")
    else:
        await message.answer("❌ Что-то пошло не так при активации промокода!")

@dp.callback_query_handler(text="delete_promo")
async def delete_promo_callback(message: types.Message):
    await logAction(delete_promo_callback, True, message)
    registered = userRegister(message.from_user.id)
    is_trusted = isUserTrustedPerson(message.from_user.id)
    if registered and is_trusted:
        await message.answer("🔏 Введите ID промокода в базе данных")
        await DeletePromo.id.set()

@dp.message_handler(state=DeletePromo.id)
async def process_promo_id(message: types.Message, state: FSMContext):
    await logAction(process_promo_id, True, message)
    await state.finish()
    try:
        int(message.text)
    except:
        return await message.answer(text=f"<b>Значение ID должно быть целочисленным!</b>", parse_mode="HTML")
    deleting_promo = promocode.Promo.delete_promo(message.text)
    if deleting_promo:
        await message.answer(text=f"<b>Промокод удален успешно!</b>", parse_mode="HTML")
    else:
        await message.answer(text=f"<b>Что-то пошло не так при удалении промокода!</b>", parse_mode="HTML")

@dp.callback_query_handler(text="create_promo")
async def create_promo_callback(message: types.Message):
    await logAction(create_promo_callback, True, message)
    registered = userRegister(message.from_user.id)
    is_trusted = isUserTrustedPerson(message.from_user.id)
    if registered and is_trusted:
        await message.answer("🔏 Введите новый промокод в формате body-description-item_id-usages ")
        await NewPromo.body.set()


@dp.message_handler(state=NewPromo.body)
async def process_promo_body(message: types.Message, state: FSMContext):
    await logAction(process_promo_body, True, message)
    await state.finish()
    text = message.text
    split_promo = text.split("-")
    try:
        int(split_promo[2])
        int(split_promo[3])
    except:
        return await message.answer(text=f"<b>Промокод указан не по шаблону!</b>", parse_mode="HTML")
    if len(split_promo) == 4:
        creating_promo = promocode.Promo.create_promo(message.from_user.id, split_promo[0], split_promo[1], split_promo[2], split_promo[3])
        if creating_promo[0]:
            await message.answer(text=f"Создан промокод <b>{creating_promo[1]}</b>", parse_mode="HTML")
        else:
            await message.answer(text=f"<b>Произошла ошибка при создании промокода</b>", parse_mode="HTML")
    else:
        await message.answer(text=f"<b>Промокод указан не по шаблону!</b>", parse_mode="HTML")


@dp.message_handler(commands=["profile"])
async def profile(message: types.Message):
    await logAction(profile, True, message)
    registered = userRegister(message.from_user.id)
    cursor.execute("SELECT available_answers FROM users WHERE telegram_id = ?", (str(message.from_user.id),))
    result = cursor.fetchone()
    if result and registered:
        text = f"""
👤 Пользователь: {message.from_user.username}

📌 Ответов доступно: {result[0]}
💳 Купить ответы - /buy_answers
"""
        await message.answer(text)
    else:
        await message.answer("❌ Что-то пошло не так. Попробуй позже!")

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await logAction(start, True, message)
    text = f"""🔹 SkySmartHack - это бот, который даст тебе ответы на любой тест платформы SkySmart. Просто отправь боту ссылку на тест, чтобы получить их.

📺 Официальный телеграм-канал бота: https://t.me/skysmarthack
💡 Сообщество ВК разработчиков бота: https://vk.com/belgrays

💳 Пополнить количество доступных ответов - /buy_answers
🔑 Активировать промокод - /promo
👤 Посмотреть свой профиль - /profile
ℹ️ Информация о боте - /start

💻 Репозиторий бота: https://github.com/BelGray/SkySmartHack"""
    await message.answer(text, reply_markup=keyboard_client)

@dp.message_handler()
async def message_handler(message: types.Message):
    await logAction(message_handler, True, message)
    hash_url = SSApi.cut_hash(message["text"])
    user_register = userRegister(str(message.from_user.id))
    if hash_url[0] and user_register:
        try:
            test_ids = SSApi.get_tasks(hash_url[1])
            test_meta = SSApi.get_meta(hash_url[1])
            await message.answer(
                f"""📘 <b>{test_meta[0]}</b>\n📝 {test_meta[1]}\n\n✏️ Заданий: {len(test_ids)}\n🆔 Код теста: {hash_url[1]}""",
                parse_mode="HTML",
                reply_markup=skysmarthack.buttons.ButtonClient)

        except Exception as e:
            await message.answer(
                f"""⭕ <b>Данного теста не существует. Возможно, ты допустил ошибку при копировании ссылки.</b>""",
                parse_mode="HTML")

    elif message["text"] not in commands_list:
        await message.answer(
            f"""🖇️ <b>Отправь рабочую ссылку на тест SkySmart</b>""",
            parse_mode="HTML")


@dp.callback_query_handler(text="get_answers_button")
async def get_answers_callback(message: types.Message):
    await logAction(get_answers_callback, True, message)
    chat_id = message["message"]["chat"]["id"]
    message_content = message["message"]["text"]
    hash_url = (True, message_content[-10:])
    user_register = userRegister(str(message["from"]["id"]))
    if hash_url[0] and user_register:
        cursor.execute(f"""SELECT available_answers FROM users WHERE telegram_id = ?""", (str(message["from"]["id"]),))
        available_answers = cursor.fetchone()
        if int(available_answers[0]) > 0:
            answer_obj = TaskAnswerObject(hash_url[1])
            full_answers = answer_obj.get_answers()
            for i in range(len(full_answers)):
                task_dict = full_answers[i]
                await bot.send_message(chat_id=chat_id, text=f"✏️ <b>Задание №{i+1}</b>\n{task_dict['full_q']}\n\n📌 <b>Ответ:\n{' '.join(task_dict['answer'])}</b>",
                                     parse_mode="HTML")
            else:
                try:
                    cursor.execute("UPDATE users SET available_answers = available_answers - 1 WHERE telegram_id = ?", (str(message["from"]["id"]),))
                    bot_db.commit()
                except:
                    pass
        else:
            await bot.send_message(
            chat_id=chat_id,
            text=f"⁉️ <b>У тебя закончилось количество доступных ответов на тесты.</b>\n\n🔑 Активируй промокод, используя команду /promo\n💳 Или купи ответы при помощи команды /buy_answers",
            parse_mode="HTML")
    else:
        await bot.send_message(chat_id=chat_id,
                               text=f"❌ <b>Что-то пошло не так при получении ответов. Попробуй повторить попытку позже или сообщи об этом в @skysmarthack</b>",
                               parse_mode="HTML")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
