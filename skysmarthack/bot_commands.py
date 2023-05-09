from aiogram import types

async def set_default_commands(dp):
    """Команды telegram бота"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Главное меню бота")
        ]
    )