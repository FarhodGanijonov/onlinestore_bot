import os
import django

# 1. Django sozlamalarini yuklash — ILK ISH
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

from shop.models import Category

router = Router()


async def get_main_categories_keyboard():
    categories = await sync_to_async(list)(Category.objects.filter(parent=None))

    buttons = []
    for category in categories:
        buttons.append([
            InlineKeyboardButton(
                text=category.name_uz,  # Keyinchalik tilga qarab tanlanadi
                callback_data=f"category_{category.id}"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.callback_query(F.data.startswith("category_"))
async def show_subcategories(callback: types.CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    subcategories = await sync_to_async(list)(
        Category.objects.filter(parent_id=category_id)
    )

    if subcategories:
        buttons = [
            [InlineKeyboardButton(text=sub.name_uz, callback_data=f"category_{sub.id}")]
            for sub in subcategories
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text(
            "Quyidagi bo‘limlardan birini tanlang:", reply_markup=keyboard
        )
    else:
        await callback.answer("Bu bo‘limda hozircha mahsulotlar yo‘q", show_alert=True)
