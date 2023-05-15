import re

from database.sql_configs import cursor, bot_db
from skysmarthack.loader import bot, dp

__developers = ["1066757578"]
__trusted_persons = [] + __developers
def userRegister(user_telegram_id) -> bool:
    """Зарегистрировать пользователя в базу данных, если его там нет"""
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = ?", (str(user_telegram_id),))
    result = cursor.fetchone()
    if not result:
        try:
          cursor.execute(f"""
            INSERT INTO users VALUES(
            NULL,
            '{str(user_telegram_id,)}',
            '{0}',
            '0',
            '{2}'
            )
            """)
          bot_db.commit()
        except Exception as e:
            print(e)
            return False
    return True

def isUserDeveloper(user_telegram_id) -> bool:
    """Проверить, является ли пользователь разработчиком бота"""
    if str(user_telegram_id) in __developers:
        return True
    return False

def isUserTrustedPerson(user_telegram_id) -> bool:
    """Проверить, является ли пользователь доверенным"""
    if str(user_telegram_id) in __trusted_persons:
        return True
    return False

def isUserRegistered(user_telegram_id) -> bool:
    """Проверить, существует ли пользователь в базе данных"""
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = {str(user_telegram_id, )}")
    result = cursor.fetchone()
    if not result:
        return False
    return True

async def isUserInChannel(user_id, channel_id):
    user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    user_channel_status = re.findall(r"\w*", str(user_channel_status))
    try:
        if user_channel_status[70] != 'left':
            return "subscribed"
        else:
            return "unsubscribed"
    except:
        if user_channel_status[60] != 'left':
            return "subscribed"
        else:
            return "unsubscribed"