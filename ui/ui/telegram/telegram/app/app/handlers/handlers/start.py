from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import asyncio
from datetime import datetime
from multiprocessing import Process

from handlers.allusers import ByBitStart
from database.models.models import user
from strategies.test_strategy import Disptcher
from strategies.settings import StrategySettings
from template_messages.template_messages import *
from keyboards import buttons


engine = create_engine("sqlite:///Data.db", echo=True)
tasks = {}
router = Router()


@router.callback_query(F.data.startswith("bybit_choosestrat_"))
async def choose_strategy(callback: types.CallbackQuery, state: FSMContext):
    uid = int(callback.data.split('_')[2])
    builder = InlineKeyboardBuilder()
    builder.add(buttons.STRATEGY_CONSERVO())
    builder.add(buttons.STRATEGY_PROF())
    await callback.message.answer(text="Выберите активную пару",
                                  reply_markup=builder.as_markup())
    

@router.callback_query(F.data.startswith("strategy_conservo"))
async def strategy_conservo(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(valuemap=[
            0.2,
            0.2,
            0.4,
            0.8,
            1.6,
            3.2,
            6.4,
            12.8
        ])
    await state.update_data(stepmap=[
            0.3,
            0.8,
            1.8,
            3.2,
            6,
            10,
            15
        ])
    await state.set_state(ByBitStart.start.state)
    builder = InlineKeyboardBuilder()
    builder.add(buttons.START)
    await callback.message.answer(text="Все готово",
                                  reply_markup=builder.as_markup())
    

@router.callback_query(F.data.startswith("strategy_prof"))
async def strategy_prof(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ByBitStart.stepmap.state)
    await callback.message.answer(text="Введите Step Map через запятую")

@router.message(ByBitStart.stepmap)
async def stepmap(message: types.Message, state: FSMContext):
    text = message.text.lower()
    list1 = [float(i) for i in text.split(',')]
    await state.update_data(stepmap=list1)
    await message.answer(text="Введите Value Map через запятую")
    await state.set_state(ByBitStart.valuemap.state)

@router.message(ByBitStart.valuemap)
async def valuemap(message: types.Message, state: FSMContext):
    text = message.text.lower()
    list1 = [float(i) for i in text.split(',')]
    await state.update_data(valuemap=list1)
    builder = InlineKeyboardBuilder()
    builder.add(buttons.START)
    await message.answer(text="Все готово",
                                reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("start"))
async def start_bybit(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data or 'aid' not in user_data:
        message.answer('Выберите пользователя и API')
        return
    aid = int(user_data['aid'])
    with Session(engine) as session:
        a = session.query(user.API).filter(
            user.API.id == aid).all()[0]
        u = a.user

        sttngs = StrategySettings()
        sttngs.uid = u.id
        sttngs.api = a.bybitapi
        sttngs.secret = a.bybitsecret
        sttngs.testnet = (a.net == 'testnet')
        sttngs.leverage = 20
        sttngs.dep = a.deposit
        sttngs.stepmap = user_data['stepmap']
        sttngs.symbol = f'{a.symbol}USDT'
        sttngs.valuemap = user_data['valuemap']
        sttngs.logprefix = f'logs/{u.id}{u.name}/{a.id}{a.symbol}/{datetime.now()}.log'

        
        dp = Disptcher(sttngs)
        try:
            with Session(engine) as session:
                from multiprocessing import Process
                a = session.query(user.API).filter(
                    user.API.id == aid).all()[0]
                p = Process(target=dp.start)
                p.daemon = True
                p.name = f'TradeProcessUSER{u.id}API{aid}SYMBOL{a.symbol}'
                p.start()

                a.pid = str(p.pid)
                session.commit()
                tasks[aid] = p
        except Exception:
            print('Ошибка системы Windows призапуске многоппроцессорного режима')
            print('Запуск многопоточного режима. Остановка не работает')


@router.callback_query(F.data.startswith("bybit_stop_"))
async def start_bybit(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if 'uid' not in user_data or 'aid' not in user_data:
        message.answer('Выберите пользователя и API')
        return
    aid = int(user_data['aid'])
    with Session(engine) as session:
        a = session.query(user.API).filter(
            user.API.id == aid).all()[0]
        u = a.user

        p = tasks[a.id]
        assert type(p) == Process
        p.kill()