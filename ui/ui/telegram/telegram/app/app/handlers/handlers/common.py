from aiogram import Dispatcher, types
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from typing import Text

from keyboards import buttons as my_buttons



router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.add(my_buttons.ALL_USERS,
                my_buttons.ADD_USER,
    )

    await message.answer(
        text="Выберите следующее действие",
        reply_markup=builder.as_markup()
    )


# Нетрудно догадаться, что следующие два хэндлера можно 
# спокойно объединить в один, но для полноты картины оставим так

# default_state - это то же самое, что и StateFilter(None)
@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")