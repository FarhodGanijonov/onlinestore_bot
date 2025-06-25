# bot/handlers/start.py

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

# 🔧 TO‘G‘RI IMPORT
from bot.keyboards.reply.language import language_keyboard

from bot.states.register import RegisterState

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: types.Message, state: FSMContext):
    await state.set_state(RegisterState.language)
    await message.answer(
        "Assalomu alaykum!\n\nTilni tanlang:",
        reply_markup=language_keyboard
    )
