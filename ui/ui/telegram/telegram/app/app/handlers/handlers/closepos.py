from aiogram import Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import asyncio
from typing import Text

import database.models.models.user as user
from strategies.instruments import Instruments
from keyboards.simple_row import make_row_keyboard, make_inline_keyboard
import keyboards.buttons as buttons
from template_messages.template_messages import *


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


@router.callback_query(F.data.startswith("bybit_close_long"))
async def close_long(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    if 'aid' not in user_data:
        await callback.answer('Выберите API')
    aid = int(user_data['aid'])

    with Session(engine) as session:
        a = session.query(user.API).filter(user.API.id == aid).all()[0]
        assert type(a) == user.API
        instr = Instruments(
            (a.net == 'testnet'),
            a.bybitapi,
            a.bybitsecret,
            a.symbol + 'USDT'
        )
        instr.close_long()


@router.callback_query(F.data.startswith("bybit_close_short"))
async def close_long(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    if 'aid' not in user_data:
        await callback.answer('Выберите API')
    aid = int(user_data['aid'])

    with Session(engine) as session:
        a = session.query(user.API).filter(user.API.id == aid).all()[0]
        assert type(a) == user.API
        instr = Instruments(
            (a.net == 'testnet'),
            a.bybitapi,
            a.bybitsecret,
            a.symbol + 'USDT'
        )
        instr.close_short()
    