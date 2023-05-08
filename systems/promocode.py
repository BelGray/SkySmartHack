
import systems.decorators


class Promo:

    #Type: {id}-{body}-{item_id}

    item_ids = {
        1:{"premium":1},
        2:{"available_answers":5},
        3:{"available_answers":15},
        4:{"available_answers":25},
        5:{"available_answers":50},
        6:{"available_answers":75},
        7:{"available_answers":100},
    }

    def create_promo(self, id, body, description, item_id, usages,):
        ...

class alreadyExistsPromo:
        def __init__(self, promo, author_telegram_id):
            self.promo = str(promo)
            self.author_telegram_id = str(author_telegram_id)
            self.use_promo = systems.decorators.isValidPromo(self.promo)(self.use_promo)
        def use_promo(self):
            promo_parts = self.promo.split("-")
            id = promo_parts[0]
            body = promo_parts[1]
            item_id = promo_parts[2]



