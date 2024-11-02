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
from strategies.user_info import UserInfo
from template_messages.template_messages import *
from handlers.allusers import ByBitStart


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


@router.callback_query(F.data.startswith("traiding_pairs"))
async def traidingpairs(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    with Session(engine) as session:
        u = session.query(user.User).filter(
            user.User.id == user_data['uid']).all()[0]
        text = 'Торговые пары\n\nАктивные пары: '
        for a in u.apis:
            text += str(a.symbol) + 'USDT, '
        text += '\nВыберите пару для торговли'
        builder = InlineKeyboardBuilder()
        builder.add(buttons.ACTIVE_PAIRS())
        builder.add(buttons.ADD_TRAIDINGPAIR())

        await callback.message.answer(text=text,
                                      reply_markup=builder.as_markup())
        
    
@router.callback_query(F.data.startswith("active_pairs_"))
async def activepairs(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    with Session(engine) as session:
        builder = InlineKeyboardBuilder()
        u = session.query(user.User).filter(user.User.id == user_data['uid']).all()[0]
        for a in u.apis:
            builder.add(buttons.COINAPI(a.id, a.symbol))
        await state.set_state(ByBitStart.symbol)
        await callback.message.answer(text="Выберите активную пару",
                                      reply_markup=builder.as_markup())
        

@router.message(ByBitStart.symbol)
@router.callback_query(F.data.startswith("bybit_change2_"))
async def bybitsymbol(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(symbol=callback.data.split('_')[2].split('$')[0])
    await state.update_data(aid=callback.data.split('_')[2].split('$')[1])

    user_data = await state.get_data()
    if 'uid' not in user_data:
        await callback.answer('Выберите пользователя')
        return
    if 'aid' not in user_data:
        await callback.answer('Выберите API')
    aid = int(user_data['aid'])

    user_data = await state.get_data()
    builder = InlineKeyboardBuilder()
    row = [[buttons.STARTBYBIT(user_data["uid"])],
           [buttons.STOPBYBIT(user_data["uid"]),],
           [buttons.CLOSELONGBYBIT(), buttons.CLOSESHORTBYBIT()],
           [buttons.CHANGE_API, buttons.CHANGE_DEPOSIT],
           [buttons.DELETEAPI()], ]
    kb = InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)

    with Session(engine) as session:
        a = session.query(user.API).filter(user.API.id == aid).all()[0]
        assert type(a) == user.API
        user_info = UserInfo(
            (a.net == 'testnet'),
            a.bybitapi,
            a.bybitsecret,
            a.symbol + 'USDT'
        )
        user_info.update()

    # await state.set_state(ByBitStart.deposit.state)
    await callback.message.answer(
        text=f"""
Торговые пары
Выбрана торговая пара: {user_data["symbol"]} 
{user_info}
""",
        reply_markup=kb
    )

