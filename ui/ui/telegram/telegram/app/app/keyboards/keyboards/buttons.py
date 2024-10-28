
from aiogram import Bot, Dispatcher, Router, types


EDIT_DATA = types.InlineKeyboardButton(
    text="Редактировать данные пользователя",
    callback_data="edit"
)

ALL_USERS = types.InlineKeyboardButton(
    text="Пользователи",
    callback_data="all_users"
)

ADD_USER = types.InlineKeyboardButton(
    text="Добавить пользователя",
    callback_data="add_user"
)

STARTBYBIT1 = types.InlineKeyboardButton(
    text="Запустить ByBit",
    callback_data="bybit_start_"
)

CHANGE_API = types.InlineKeyboardButton(
    text="API ключи",
    callback_data="change_api"
)

CHANGE_DEPOSIT = types.InlineKeyboardButton(
    text="Торговый депозит",
    callback_data="change_deposit"
)

STATISTIS = types.InlineKeyboardButton(
    text="Выгрузка статистики",
    callback_data="get_stat"
)

CHOOSE_TESTNET = types.InlineKeyboardButton(
    text="Test Net",
    callback_data="choosenet_testnet"
)

CHOOSE_MAINNET = types.InlineKeyboardButton(
    text="Main Net",
    callback_data="choosenet_mainnet"
)

def ADD_TRAIDINGPAIR(uid=''):
    return types.InlineKeyboardButton(
        text="Добавить новую пару",
        callback_data=f"addtraiding_pairs_{uid}"
    )

def ACTIVE_PAIRS(uid=''):
    return types.InlineKeyboardButton(
        text="Активные пары",
        callback_data=f"active_pairs_{uid}"
    )

def TRAIDING_PAIRS(uid=''):
    return types.InlineKeyboardButton(
        text="Торговые пары",
        callback_data=f"traiding_pairs_{uid}"
    )

def STARTBYBIT(uid=''):
    return types.InlineKeyboardButton(
        text="Запустить",
        callback_data=f"bybit_choosestrat_{uid}"
    )

# def CHOOSE(uid):
#     return types.InlineKeyboardButton(
#         text="Запустить",
#         callback_data=f"bybit_start_{uid}"
#     )

def STOPBYBIT(uid=''):
    return types.InlineKeyboardButton(
        text="Остановить",
        callback_data=f"bybit_stop_{uid}"
    )


def STOPCLOSEBYBIT(uid=''):
    return types.InlineKeyboardButton(
        text="Остановить c закрытием",
        callback_data=f"bybit_stopclose_{uid}"
    )


def COIN(coin=''):
    return types.InlineKeyboardButton(
        text=coin,
        callback_data=f"bybit_change_{coin}")

# def COIN1(coin):
#     return types.InlineKeyboardButton(
#         text=coin,
#         callback_data=f"bybit_change1_{coin}")

def COINAPI(api, coin):
    return types.InlineKeyboardButton(
        text=coin,
        callback_data=f"bybit_change2_{coin}${api}")

def DELETEUSER():
    return types.InlineKeyboardButton(
        text="Удалить",
        callback_data=f"delete_user"
    )


def DELETEAPI(aid=''):
    return types.InlineKeyboardButton(
        text="Удалить",
        callback_data=f"delete_api_{aid}"
    )


def STRATEGY_CONSERVO():
    return types.InlineKeyboardButton(
        text="Консерв.(0.2%)",
        callback_data="strategy_conservo"
    )


def STRATEGY_AGRESSIVE():
    return types.InlineKeyboardButton(
        text="Агрес.(0.4%)",
        callback_data="strategy_agressive"
    )


def STRATEGY_PROF():
    return types.InlineKeyboardButton(
        text="Польз.",
        callback_data="strategy_prof"
    )
