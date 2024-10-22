from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import asyncio

from database.models.models import user
from strategies.test_strategy import Disptcher
from strategies.settings import StrategySettings
from template_messages.template_messages import *


engine = create_engine("sqlite:///Data.db", echo=True)
router = Router()


@router.callback_query(F.data.startswith("bybit_choosestrat_"))
async def start_bybit(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data or 'aid' not in user_data:
        callback.answer('Выберите пользователя и API')
        return
    aid = int(user_data['aid'])
    with Session(engine) as session:
        a = session.query(user.API).filter(
            user.API.id == aid).all()[0]
        u = a.user

        sttngs = StrategySettings()
        sttngs.api = a.bybitapi
        sttngs.secret = a.bybitsecret
        sttngs.testnet = (a.net == 'testnet')
        sttngs.leverage = 20
        sttngs.dep = a.deposit
        sttngs.stepmap = [
            0.3,
            0.8,
            1.8,
            3.2,
            6,
            10,
            15
        ]
        sttngs.symbol = f'{a.symbol}USDT'
        sttngs.valuemap = [
            0.2,
            0.2,
            0.4,
            0.8,
            1.6,
            3.2,
            6.4,
            12.8
        ]

        dp = Disptcher(sttngs)
        loop = asyncio.get_running_loop()
        loop.create_task(dp.start())