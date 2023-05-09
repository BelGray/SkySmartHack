import sqlite3
from database.sql_configs import cursor, bot_db


def isValidPromo(promo):
    """Проверить, существует ли введенный промокод"""
    def function_wrapper(function):
        def wrapper(*args, **kwargs):
            if "-" in promo and promo.count("-") == 2:
                promo_parts = promo.split("-")
                id = promo_parts[0]
                body = promo_parts[1]
                item_id = promo_parts[2]
                cursor.execute(f"SELECT * FROM promo WHERE id = '{int(id),}' AND body = '{str(body)}' AND item_id = '{int(item_id),}'")
                result = cursor.fetchone()
                if result:
                    function(*args, **kwargs)
                    return True
                if not result:
                    return False

        return wrapper
    return function_wrapper

