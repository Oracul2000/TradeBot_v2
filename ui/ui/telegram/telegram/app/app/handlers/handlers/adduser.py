from aiogram import Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from typing import Text

from database.models.models.user import *
from keyboards import buttons, simple_row

engine = create_engine("sqlite:///Data.db", echo=False)


router = Router()

coins = ['ADA', 'LINK', 'XRP', 'XLM', 'DASH', 'NEO', 'TRX',
         'EOS', 'LTC', 'DOGE', 'APT', 'ATOM', 'BTC', 'ETH']

class AddNewUser(StatesGroup):
    name = State()
    bybitapi = State()
    bybitsecret = State()
    symbol = State()
    deposit = State()


@router.message(Command("add_user"))
@router.callback_query(F.data == "add_user")
async def adduser(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Введите имя пользователя:"
    )
    await state.set_state(AddNewUser.name)


@router.message(AddNewUser.name)
async def namechoosen(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(AddNewUser.bybitapi.state)
    await message.answer("Введите API key пользователя от ByBit")


@router.message(AddNewUser.bybitapi)
async def bybitapichoosen(message: types.Message, state: FSMContext):
    await state.update_data(bybitapi=message.text)

    await state.set_state(AddNewUser.bybitsecret)
    await message.answer("Введите Secret key пользователя от ByBit")


@router.message(AddNewUser.bybitsecret)
async def bybitsecretchoosen(message: types.Message, state: FSMContext):
    await state.update_data(bybitsecret=message.text)

    await message.answer("Введите торговую пару", reply_markup=simple_row.make_inline_keyboard(coins))
    await state.set_state(AddNewUser.symbol.state)


@router.message(AddNewUser.symbol)
@router.callback_query(F.data.startswith("bybit_change_"))
async def bybitsymbol(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(symbol=callback.data.split('_')[2])

    await state.set_state(AddNewUser.deposit.state)
    await callback.message.answer("Введите желаемый депозит в usdt")


async def bybitsymbolclone(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddNewUser.deposit.state)
    await callback.message.answer("Введите желаемый депозит в usdt")


@router.message(AddNewUser.deposit)
async def bybitdeposiot(message: types.Message, state: FSMContext):
    await state.update_data(deposit=message.text.lower())
    user_data = await state.get_data()

    print(user_data)

    with Session(engine) as session:
        nu = User(name=user_data["name"])

        na = API(name=user_data["name"],
                bybitapi=user_data["bybitapi"],
                bybitsecret=user_data["bybitsecret"],
                symbol=user_data["symbol"],
                deposit=float(user_data["deposit"]))
        nu.apis = [na]
        session.add_all([nu, na,])
        session.commit()

