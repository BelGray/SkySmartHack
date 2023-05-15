from aiogram.types import *

start_button = KeyboardButton('/start')
profile_button = KeyboardButton('/profile')
buy_answers_button = KeyboardButton('/buy_answers')
promo_button = KeyboardButton('/promo')

keyboard_client = ReplyKeyboardMarkup()
keyboard_client.add(start_button).add(promo_button).add(buy_answers_button).add(profile_button)