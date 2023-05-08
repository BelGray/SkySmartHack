from database.sql_configs import cursor, bot_db
def userRegister(user_telegram_id) -> bool:
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = {str(user_telegram_id, )}")
    result = cursor.fetchone()
    if not result:
        try:
          cursor.execute(f"""
            INSERT INTO users VALUES(
            NULL,
            '{str(user_telegram_id,)}',
            '{0}',
            '0',
            '{5}'
            )
            """)
          bot_db.commit()
        except:
            return False
    return True

def isUserRegistered(user_telegram_id) -> bool:
    cursor.execute(f"SELECT * FROM users WHERE telegram_id = {str(user_telegram_id, )}")
    result = cursor.fetchone()
    if not result:
        return False
    return True