import sqlite3
#Подключение к базе данных
bot_db = sqlite3.connect("database/bot.db")
cursor = bot_db.cursor()

