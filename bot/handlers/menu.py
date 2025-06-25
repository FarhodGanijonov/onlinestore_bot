import os

from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from aiogram.types import FSInputFile
from shop.models import Category, Product
from bot.keyboards.inline.category import get_main_categories_keyboard

router = Router()

# 🛍 Mahsulotlar tugmasi bosilganda
@router.message(F.text == "🛍 Mahsulotlar")
async def show_main_categories(message: types.Message):
    keyboard = await get_main_categories_keyboard()
    await message.answer("Mahsulot kategoriyalaridan birini tanlang:", reply_markup=keyboard)

# 📦 Buyurtmalar tugmasi
@router.message(F.text == "📦 Buyurtmalar")
async def show_orders(message: types.Message):
    await message.answer("🧾 Sizning buyurtmalaringiz ro‘yxati bo‘sh.")

# ⚙ Sozlamalar tugmasi
@router.message(F.text == "⚙ Sozlamalar")
async def show_settings(message: types.Message):
    await message.answer("⚙ Sozlamalar bo‘limidasiz. Tez orada imkoniyatlar qo‘shiladi.")

# Kategoriya bosilganda subkategoriya yoki mahsulot chiqadi
@router.callback_query(F.data.startswith("category_"))
async def show_subcategories_or_products(callback: types.CallbackQuery):
    category_id = int(callback.data.split("_")[1])

    # Subkategoriyalar mavjudmi?
    subcategories = await sync_to_async(list)(Category.objects.filter(parent_id=category_id))
    if subcategories:
        buttons = [
            [InlineKeyboardButton(text=sub.name_uz, callback_data=f"category_{sub.id}")]
            for sub in subcategories
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text("Quyidagi bo‘limlardan birini tanlang:", reply_markup=keyboard)
        return

    # Mahsulotlar mavjudmi?
    products = await sync_to_async(list)(Product.objects.filter(categories__id=category_id))
    if products:
        buttons = [
            [InlineKeyboardButton(text=product.name_uz, callback_data=f"product_{product.id}")]
            for product in products
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text("Mahsulotlardan birini tanlang:", reply_markup=keyboard)
        return

    # Hech narsa topilmasa
    await callback.answer("Bu bo‘limda hozircha hech narsa yo‘q", show_alert=True)



# Mahsulot tugmasi bosilganda tafsilotlar ko‘rsatish
@router.callback_query(F.data.startswith("product_"))
async def show_product_detail(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    product = await sync_to_async(Product.objects.get)(id=product_id)

    image_path = product.main_image.path  # bu rasmning lokal yo'li
    if not os.path.exists(image_path):
        await callback.message.answer("❌ Rasm topilmadi.")
        return

    caption = f"<b>{product.name_uz}</b>\n\n{product.description_uz or ''}\n\n💰 Narxi: {product.price} so‘m"
    photo = FSInputFile(image_path)

    # 🔘 Savatchaga qo‘shish tugmasi
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Savatchaga qo‘shish", callback_data=f"add_to_cart_{product.id}")]
        ]
    )


    await callback.message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

# Savatni vaqtincha RAM da saqlash uchun (foydalanuvchi_id orqali)
cart = {}

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: types.CallbackQuery):
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    # Mahsulotni olish
    product = await sync_to_async(Product.objects.get)(id=product_id)

    # Savatga qo‘shish
    if user_id not in cart:
        cart[user_id] = []

    cart[user_id].append({
        "id": product.id,
        "name": product.name_uz,
        "price": product.price
    })

    await callback.answer("✅ Mahsulot savatchaga qo‘shildi", show_alert=True)

# 🛒 Savatchani ko‘rish
@router.message(F.text == "🛒 Savatcha")
async def show_cart(message: types.Message):
    user_id = message.from_user.id

    if user_id not in cart or not cart[user_id]:
        await message.answer("🛒 Savatchangiz hozircha bo‘sh.")
        return

    text = "🛒 <b>Savatchangiz:</b>\n\n"
    total = 0

    for item in cart[user_id]:
        text += f"• {item['name']} - {item['price']} so‘m\n"
        total += item['price']

    text += f"\n<b>Jami:</b> {total} so‘m"

    await message.answer(text, parse_mode="HTML")








