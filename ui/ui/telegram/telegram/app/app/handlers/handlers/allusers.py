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


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


class ByBitStart(StatesGroup):
    uid = State()
    symbol = State()
    deposit = State()
    stop = State()
    uservalue = State()
    gofromadding = State()
    beforedate = State()
    afterdate = State()
    statistics = State()


@router.message(Command("all_users"))
@router.callback_query(F.data == "all_users")
async def allusers(callback: types.CallbackQuery, state: FSMContext):
    with Session(engine) as session:
        all_users = session.query(user.User).all()
        textanswer = ""
        print(all_users)
        for u in all_users:
            textanswer += useroutput(u) + '\n'
        await callback.message.answer(
                text=textanswer,
            )
        await callback.message.answer(
                text="Введите порядковый номер пользователя"
            )
    await state.set_state(ByBitStart.uid.state)


@router.message(ByBitStart.uid)
async def bybitdeposiot(message: types.Message, state: FSMContext):
    await state.update_data(uid=int(message.text.lower()))
    user_data = await state.get_data()
    with Session(engine) as session:
        u = session.query(user.User).filter(
            user.User.id == int(user_data["uid"])).all()[0]
        text = f'Параметры пользователя {u.name}#{u.id}\n'
        for a in u.apis:
            # ti = TradeInfo.SmallBybit(a.bybitapi, a.bybitsecret)
            # ti.update(a)
            # text += msgs.userbigouput(a, ti)
            text += "\nIN PROGRESS\n"
        builder = InlineKeyboardBuilder()
        builder.add(buttons.TRAIDING_PAIRS())
        builder.add(buttons.DELETEUSER())
        builder.add(buttons.STATISTIS)
        if text:
            await message.answer(text=text,
                             reply_markup=builder.as_markup())
        else:
            await message.answer("Сначала создайте нового пользователя")
