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


@router.callback_query(F.data.startswith("delete_user"))
async def change_api(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    uid = int(user_data['uid'])
    with Session(engine) as session:
        session.query(user.User).filter(user.User.id == uid).delete()
        session.commit()
    await callback.message.answer("Пользователь удален")


@router.callback_query(F.data.startswith("delete_api"))
async def change_api(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    if 'aid' not in user_data:
        await callback.answer('Выберите API')
    aid = int(user_data['aid'])
    with Session(engine) as session:
        session.query(user.API).filter(user.API.id == aid).delete()
        session.commit()
    await callback.message.answer("API удалена")




    