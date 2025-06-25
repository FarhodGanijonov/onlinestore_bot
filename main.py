import os
import asyncio
import django

from bot.keyboards.inline import category

# Django settings ini yuklab olish (eng avval)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Aiogram importlar
from aiogram import Dispatcher
from bot.config import bot
from bot.handlers import start, register, menu  # Routerlar shu yerda

async def main():
    dp = Dispatcher()

    # Routerlarni qo‘shamiz
    dp.include_router(start.router)
    dp.include_router(register.router)
    dp.include_router(menu.router)
    dp.include_router(category.router)
    # Botni ishga tushuramiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
