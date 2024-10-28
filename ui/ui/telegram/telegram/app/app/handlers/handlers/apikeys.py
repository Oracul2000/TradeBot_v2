from aiogram import Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import database.models.models.user as user

import asyncio
from typing import Text

from keyboards.simple_row import make_row_keyboard, make_inline_keyboard
import keyboards.buttons as buttons
from template_messages.template_messages import *
from handlers.adduser import AddNewUser


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


@router.callback_query(F.data.startswith("change_api"))
async def change_api(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    if 'aid' not in user_data:
        await callback.answer('Выберите API')
    builder = InlineKeyboardBuilder()
    builder.add(buttons.CHOOSE_MAINNET)
    builder.add(buttons.CHOOSE_TESTNET)
    await callback.message.answer("Выберите сеть",
                        reply_markup=builder.as_markup())
    await state.set_state(AddNewUser.bybitnet)
