import asyncio
import uuid
import pyqiwip2p
from pyqiwip2p.p2p_types import Bill
from database.sql_configs import *
from systems.tool_methods import *
from pyqiwip2p import QiwiP2P

class QiwiPayment:
    def __init__(self, qiwi_token):
        self.qiwi_token = qiwi_token
        self.qiwi = QiwiP2P(auth_key=self.qiwi_token)

    async def buildBill(self, user_telegram_id: str, count: int, amount: int, comment: str, bill_lifetime) -> tuple:
        """Сконструировать счёт"""
        register = userRegister(user_telegram_id)
        if register:
            try:
                lifetime = bill_lifetime #минут
                bill_id = str(uuid.uuid4()) + "_user_telegram_id:" + user_telegram_id + "_skysmarthack"
                bill: Bill = self.qiwi.bill(bill_id=bill_id, amount=amount, lifetime=lifetime, comment=comment)
                url = bill.pay_url
                print(f"""----------------------------------------------
Создан счет на оплату QIWI

ID пользователя: {user_telegram_id}
Сумма: {amount} руб.
Срок: {lifetime} мин.
ID счета: {bill_id}
URL счета: {url}""")
                return True, url, bill_id, count

            except Exception as e:
                print(e)
                return False, None, None, None

        else:
            return False, None, None, None

    async def waitForPay(self, user_telegram_id, bill_id, count) -> bool:
        """Ожидание оплаты счета, построенного в методе buildBill()"""
        while True:
            await asyncio.sleep(20)
            status = self.qiwi.check(bill_id=bill_id).status
            if status == "EXPIRED":
                self.qiwi.reject(bill_id=bill_id)
                print(f"""----------------------------------------------
🕓 У счета истек срок!

ID счета: {bill_id}
ID пользователя: {user_telegram_id}""")
                return False
            elif status == "PAID":
                cursor.execute(f"""
                SELECT * FROM users WHERE telegram_id = ?
                """, (str(user_telegram_id),))
                result = cursor.fetchone()
                if result:
                    try:
                        cursor.execute(f"""
                        UPDATE users SET 
                        available_answers = available_answers + ?
                        WHERE telegram_id = ?
                        """, (count, str(user_telegram_id)))
                        bot_db.commit()
                        print(f"""----------------------------------------------
✅ Счет успешно оплачен! Товар выдан: {count} ответов

ID пользователя: {user_telegram_id}
ID счета: {bill_id}
""")
                        return True
                    except Exception as e:
                        print(f"""----------------------------------------------
❌ ОШИБКА ПРИ ВЫДАЧЕ ТОВАРА ПОЛЬЗОВАТЕЛЮ! Не выдан товар: {count} ответов

ID пользователя: {user_telegram_id}
ID счета: {bill_id}
Ошибка: {e}""")
                        return False
                else:
                    return False



