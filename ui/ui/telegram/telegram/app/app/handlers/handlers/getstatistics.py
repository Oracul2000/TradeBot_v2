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
from handlers.allusers import ByBitStart
from strategies.user_info import UserInfo


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


@router.callback_query(F.data == "get_stat")
async def beforedate(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите дату ОТ"
    )
    await state.set_state(ByBitStart.beforedate)


@router.message(ByBitStart.beforedate)
async def afterdate(message: types.Message, state: FSMContext):
    await state.update_data(startTime=message.text)

    await state.set_state(ByBitStart.afterdate.state)
    await message.answer("Введите дату ДО")


@router.message(ByBitStart.afterdate)
async def get_stat(message: types.Message, state: FSMContext):
    await state.update_data(stopTime=message.text)
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await message.answer('Выберите пользователя')
        return
    uid = int(user_data['uid'])

    with Session(engine) as session:
        u = session.query(user.User).filter(user.User.id == uid).all()[0]
        for a in u.apis:
            user_info = UserInfo(
            (a.net == 'testnet'),
            a.bybitapi,
            a.bybitsecret,
            a.symbol + 'USDT'
            )
            user_info.update()
            user_info.statistics(
                a.symbol + 'USDT', startTime=user_data["startTime"], stopTime=user_data["stopTime"])
            from aiogram.types import FSInputFile

            doc = FSInputFile(path='./out.csv', filename=f'{a.symbol}.csv')
            await message.answer_document(document=doc)
