# bot/keyboards/reply/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Mahsulotlar")],
        [KeyboardButton(text="🛒 Savatni ko\'rish"), KeyboardButton(text="🧹 Savatni tozalash")],
        [KeyboardButton(text="⚙ Sozlamalar")],
    ],
    resize_keyboard=True
)
