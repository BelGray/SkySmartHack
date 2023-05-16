from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ButtonClient = InlineKeyboardMarkup(row_width=2)
ToolsMenuButtonClient = InlineKeyboardMarkup(row_width=2)
ActivatePromoButtonClient = InlineKeyboardMarkup(row_width=2)

activate_promo_button = InlineKeyboardButton(text="✔️ Активировать", callback_data="activate_promo_button")
get_answers_button = InlineKeyboardButton(text="📌 Получить ответы", callback_data="get_answers_button")
create_promo = InlineKeyboardButton(text="Создать промокод", callback_data="create_promo")
delete_promo = InlineKeyboardButton(text="Удалить промокод", callback_data="delete_promo")

BuyAnswersButtonClient = InlineKeyboardMarkup(row_width=2)
buy_10_answers = InlineKeyboardButton(text="10 ответов", callback_data="buy_10_answers")
buy_25_answers = InlineKeyboardButton(text="25 ответов", callback_data="buy_25_answers")
buy_50_answers = InlineKeyboardButton(text="50 ответов", callback_data="buy_50_answers")
buy_75_answers = InlineKeyboardButton(text="75 ответов", callback_data="buy_75_answers")
buy_100_answers = InlineKeyboardButton(text="100 ответов", callback_data="buy_100_answers")
BuyAnswersButtonClient.insert(buy_10_answers)
BuyAnswersButtonClient.insert(buy_25_answers)
BuyAnswersButtonClient.insert(buy_50_answers)
BuyAnswersButtonClient.insert(buy_75_answers)
BuyAnswersButtonClient.insert(buy_100_answers)

ToolsMenuButtonClient.insert(create_promo)
ToolsMenuButtonClient.insert(delete_promo)

ActivatePromoButtonClient.insert(activate_promo_button)

ButtonClient.insert(get_answers_button)