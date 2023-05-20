import datetime
import aiogram.types


async def defName(function):
    return function.__name__
async def logAction(event, output: bool, message_object: aiogram.types.Message) -> dict:
    event_name = await defName(event)
    date = datetime.datetime.now()
    if output:
        print(f"""
----------------------------------------------
ID пользователя: {message_object.from_user.id}
Имя пользователя: {message_object.from_user.full_name}
ID чата: {message_object.chat.id if "callback" not in event_name else None}
Имя чата: {message_object.chat.full_name if "callback" not in event_name else None}
Вызвана функция: {event_name}
Текст сообщения: {message_object.text if "callback" not in event_name else None}
Дата: {date}""")

    return {
        "user_id":message_object.from_user.id,
        "user_name":message_object.from_user.full_name,
        "chat_id":message_object.chat.id if "callback" not in event_name else None,
        "chat_name":message_object.chat.full_name if "callback" not in event_name else None,
        "function_name":event_name,
        "message_text":message_object.text if "callback" not in event_name else None,
        "date":date
    }