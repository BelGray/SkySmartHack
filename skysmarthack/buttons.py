from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ButtonClient = InlineKeyboardMarkup(row_width=2)
ToolsMenuButtonClient = InlineKeyboardMarkup(row_width=2)
ActivatePromoButtonClient = InlineKeyboardMarkup(row_width=2)

activate_promo_button = InlineKeyboardButton(text="Активировать", callback_data="activate_promo_button")
get_answers_button = InlineKeyboardButton(text="Получить ответы", callback_data="get_answers_button")
create_promo = InlineKeyboardButton(text="Создать промокод", callback_data="create_promo")
delete_promo = InlineKeyboardButton(text="Удалить промокод", callback_data="delete_promo")

ToolsMenuButtonClient.insert(create_promo)
ToolsMenuButtonClient.insert(delete_promo)

ActivatePromoButtonClient.insert(activate_promo_button)

ButtonClient.insert(get_answers_button)