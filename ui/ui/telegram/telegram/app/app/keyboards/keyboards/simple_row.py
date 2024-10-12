from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.buttons import *


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_inline_keyboard(items: list[str]) -> InlineKeyboardMarkup:
    row = [[COIN(i) for i in items[0: 4]],
           [COIN(i) for i in items[4: 8]],
           [COIN(i) for i in items[8: 12]],
           [COIN(i) for i in items[12:]]]
    return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)

# def make_inline_keuboard_com(items: list[str]) -> InlineKeyboardMarkup:
#     row =


# def make_inline_keyboard_BINGX(items: list[str]) -> InlineKeyboardMarkup:
#     row = [[COIN_BINGX(i) for i in items[0: 4]],
#            [COIN_BINGX(i) for i in items[4: 8]],
#            [COIN_BINGX(i) for i in items[8: 12]],]
#     return InlineKeyboardMarkup(inline_keyboard=row, resize_keyboard=True)