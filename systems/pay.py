import asyncio
import uuid
import pyqiwip2p
from pyqiwip2p.p2p_types import Bill
from database.sql_configs import *
from systems.tool_methods import *
from pyqiwip2p import QiwiP2P

class QiwiPayment:
    def __init__(self, qiwi_token, price):
        self.qiwi_token = qiwi_token
        self.price = price
        self.qiwi = QiwiP2P(auth_key=self.qiwi_token)

    def buildBill(self, user_telegram_id: str, count: int) -> tuple:
        """Сконструировать счёт"""
        register = userRegister(user_telegram_id)
        if register:
            try:
                amount = count * self.price
                lifetime = 10 #минут
                bill_id = str(uuid.uuid4()) + "_user_telegram_id:" + user_telegram_id
                bill: Bill = self.qiwi.bill(bill_id=bill_id, amount=amount, lifetime=lifetime)
                url = bill.pay_url
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
                        return True
                    except Exception as e:
                        print(e)
                        return False
                else:
                    return False



