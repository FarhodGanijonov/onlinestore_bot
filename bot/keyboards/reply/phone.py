# bot/keyboards/reply/phone.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
