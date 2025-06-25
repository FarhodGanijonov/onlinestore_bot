# bot/keyboards/reply/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Mahsulotlar")],
        [KeyboardButton(text="🛒 Savatcha"), KeyboardButton(text="⚙ Sozlamalar")],  # ✅ BU YER TO‘G‘RILANDI
    ],
    resize_keyboard=True
)
