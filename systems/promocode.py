import systems.decorators
from systems.tool_methods import userRegister, isUserDeveloper
from database.sql_configs import cursor, bot_db

class Promo:

    #Type: {id}-{body}-{item_id}

    def create_promo(self, user_telegram_id: str, body: str, description: str, item_id: int, usages: int) -> bool:
        """Создать новый промокод"""
        user_developer_check = isUserDeveloper(user_telegram_id)
        if user_developer_check:
            cursor.execute(
                f"SELECT * FROM promo WHERE body = '{str(body)}' AND item_id = '{int(item_id),}'")
            result = cursor.fetchone()
            if not result:
                try:
                    cursor.execute(f"""
                    INSERT INTO promo VALUES(
                    NULL,
                    '{body,}',
                    '{description,}',
                    '{item_id}',
                    '{usages}'
                    ) 
                    """)
                    bot_db.commit()
                    return True
                except Exception as e:
                    print(e)
                    return False
            else:
                return False
        else:
            return False

class alreadyExistsPromo:

        item_ids = {
            1: {"available_answers": 1},
            2: {"available_answers": 5},
            3: {"available_answers": 15},
            4: {"available_answers": 25},
            5: {"available_answers": 50},
            6: {"available_answers": 75},
            7: {"available_answers": 100},
        }

        def __init__(self, promo, author_telegram_id):
            self.promo = str(promo)
            self.author_telegram_id = str(author_telegram_id)
            self.use_promo = systems.decorators.isValidPromo(self.promo)(self.use_promo)

        def use_promo(self) -> bool:
            """Использовать промокод"""
            promo_parts = self.promo.split("-")
            id = int(promo_parts[0])
            body = promo_parts[1]
            item_id = int(promo_parts[2])
            register = userRegister(self.author_telegram_id)
            if register:
                cursor.execute(f"SELECT * FROM users WHERE telegram_id = {str(self.author_telegram_id),}")
                result = cursor.fetchone()
                if result:
                    try:
                        cursor.execute(f"""
                        UPDATE users SET 
                            available_answers = available_answers + {self.item_ids[item_id]["available_answers"]}
                            WHERE telegram_id = {self.author_telegram_id}
                        """)
                        bot_db.commit()

                        cursor.execute(f"""
                        UPDATE promo SET
                            usages = usages - 1
                            WHERE id = {id}
                        """)
                        bot_db.commit()
                        return True
                    except Exception as e:
                        print(e)
                        return False
                else:
                    return False
            else:
                return False







