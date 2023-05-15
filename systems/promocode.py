import systems.decorators
from systems.tool_methods import userRegister, isUserDeveloper, isUserTrustedPerson
from database.sql_configs import cursor, bot_db

class Promo:

    #Type: {id}-{body}-{item_id}

    def delete_promo(id: int) -> bool:
        """Удалить промокод из базы данных"""
        cursor.execute(f"""SELECT * FROM promo WHERE id = ?""", (int(id),))
        result = cursor.fetchone()
        if result:
            try:
                cursor.execute(f"""DELETE FROM promo WHERE id = ?""", (int(id),))
                bot_db.commit()
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False

    def create_promo(user_telegram_id, body, description, item_id: int, usages: int) -> tuple:
        """Создать новый промокод"""
        user_trusted_check = isUserTrustedPerson(str(user_telegram_id))
        if user_trusted_check:
            cursor.execute(
                f"SELECT * FROM promo WHERE body = ? AND item_id = ?", (str(body), int(item_id),))
            result = cursor.fetchone()
            if not result:
                try:
                    cursor.execute(f"""
                    INSERT INTO promo VALUES(
                    NULL,
                    ?,
                    ?,
                    ?,
                    ?
                    )
                    """, (str(body), str(description), item_id, usages))
                    bot_db.commit()
                    cursor.execute(
                        f"SELECT * FROM promo WHERE body = ? AND item_id = ?", (str(body), int(item_id),))
                    result = cursor.fetchone()
                    return True, f"{result[0]}-{result[1]}-{result[3]}"
                except Exception as e:
                    print(e)
                    return False, None
            else:
                print("promo already exists")
                return False, None
        else:
            print("user is not trusted")
            return False, None

class AlreadyExistsPromo:

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

        def get_promo_info(self):
            """Получить информацию о промокоде"""
            try:
                promo_parts = self.promo.split("-")
                id = int(promo_parts[0])
                body = str(promo_parts[1])
                item_id = int(promo_parts[2])
                register = userRegister(self.author_telegram_id)
                if register:
                    cursor.execute(f"SELECT * FROM promo WHERE id = ?", (id,))
                    result = cursor.fetchone()
                    if result:
                        return True, result
                    else:
                        print("promo is not found :(")
                        return False, None
                else:
                    print("user unregistered")
                    return False
            except Exception as e:
                print(e)
                return False, None


        def use_promo(self) -> bool:
          """Использовать промокод"""
          try:
            promo_parts = self.promo.split("-")
            id = int(promo_parts[0])
            body = str(promo_parts[1])
            item_id = int(promo_parts[2])
            register = userRegister(self.author_telegram_id)
            if register:
                cursor.execute(f"SELECT * FROM users WHERE telegram_id = ?", (str(self.author_telegram_id),))
                result = cursor.fetchone()
                if result:
                        cursor.execute(f"""
                        UPDATE users SET 
                            available_answers = available_answers + ?
                            WHERE telegram_id = ?
                        """, (int(self.item_ids[item_id]["available_answers"]), str(self.author_telegram_id),))
                        bot_db.commit()

                        cursor.execute(f"""
                        UPDATE promo SET
                            usages = usages - 1
                            WHERE id = ?
                        """, (id,))
                        bot_db.commit()
                        return True
                else:
                    print("promo doesn't exists")
                    return False
            else:
                print("user unregistered")
                return False
          except Exception as e:
              print(e)
              return False





