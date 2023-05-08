#Подключение к базе данных
import sqlite3

bot_db = sqlite3.connect("database/bot.db")
cursor = bot_db.cursor()