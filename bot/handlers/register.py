from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from bot.states.register import RegisterState
from bot.keyboards.reply.phone import phone_keyboard
from bot.keyboards.reply.main_menu import main_menu_keyboard
from users.models import TelegramUser

router = Router()

@router.message(F.text.in_({"🇺🇿 UZ", "🇷🇺 RU"}))
async def choose_language(message: types.Message, state: FSMContext):
    lang = "uz" if message.text == "🇺🇿 UZ" else "ru"
    await state.update_data(language=lang)
    await message.answer("Ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterState.full_name)


@router.message(RegisterState.full_name)
async def get_full_name(message: types.Message, state:FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Iltimos, telefon raqamingizni yuboring:", reply_markup=phone_keyboard)
    await state.set_state(RegisterState.phone_number)


@router.message(F.contact)
async def get_phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")

    # Django ORM ni async ichida chaqirish uchun sync_to_async ishlatamiz
    await sync_to_async(TelegramUser.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "full_name": message.from_user.full_name,
            "phone_number": message.contact.phone_number,
            "language": language,
        }
    )

    await message.answer("✅ Ro'yxatdan o'tdingiz!")
    await state.clear()

    await message.answer("Bo'limni tanlang:", reply_markup=main_menu_keyboard)


@router.message(RegisterState.language)
async def set_language(message: types.Message, state: FSMContext):
    # Bu yerda tanlanga n tilni olish va saqlashni yozsang bo'ladi
    await state.clear()  # holatni yakunlash
    await message.answer("🔸 Til tanlandi. Asosiy menyudan foydalaning:", reply_markup=main_menu_keyboard)
