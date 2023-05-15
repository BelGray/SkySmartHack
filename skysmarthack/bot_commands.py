from aiogram import types

commands_list = ["/start", "/promo", "/buy_answers", "/profile", "/tools"]

async def set_default_commands(dp):
    """Команды telegram бота"""
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "ℹ️ Информация о боте"),
            types.BotCommand("promo", "🔑 Активировать промокод"),
            types.BotCommand("buy_answers", "💳 Купить ответы на тесты SkySmart"),
            types.BotCommand("profile", "👤 Профиль пользователя"),
            types.BotCommand("tools", "⚙️ Панель управления ботом")
        ]
    )