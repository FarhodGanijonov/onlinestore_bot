# bot/keyboards/reply/language.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 UZ"), KeyboardButton(text="🇷🇺 RU")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
