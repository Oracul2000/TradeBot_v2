import asyncio

from bybit.constants import *
from .instruments import Instruments
from .positions import *
from bybit.settings import *
from .settings import StrategySettings


class PositionInfo():
    symbol = ''
    positions = 0
    orders = 0
    tps = 0

    def __repr__(self) -> str:
        return f'{self.symbol}: Позиций: {self.positions}, Ордеров: {self.orders}, ТП: {self.tps}'
    

class UserInfo():
    def __init__(self, testnet, api, secret, symbol):
        self.pairs = {}  # symbol: SmallPosition
        self.instr = Instruments(testnet, api, secret, symbol)

        self.symbol = symbol
        self.coin_control = {}
        self.balance = 0
        self.apiStatus = None

    def update(self, symbol):
        try:
            posinfo = PositionInfo()
            self.balance = self.instr.get_balance()
            positions = self.instr.positions_info()
            for pos in positions:
                if pos['avgPrice'] and pos['avgPrice'] != '0':
                    posinfo.positions += 1
                if pos['takeProfit']:
                    posinfo.tps += 1
            self.coin_control[symbol] = posinfo

            resp = self.instr.get_limit_orders()
            print(symbol, resp)
            if resp:
                self.coin_control[symbol].orders = len(resp) - self.coin_control[symbol].tps
            self.apiStatus = True
        except Exception as e:
            self.apiStatus = False
            print('Api неверные')

    def monitoring(self):
        answer = ""
        for i in self.coin_control:
            if "Позиций: 0" not in str(self.coin_control[i]):
                answer += str(self.coin_control[i]) + '\n'
        return answer
        

