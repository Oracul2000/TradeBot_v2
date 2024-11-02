import asyncio

from bybit.constants import *
from .instruments import Instruments
from .positions import *
from bybit.settings import *
from .settings import StrategySettings


class LimitInfo():
    def __init__(self, o) -> None:
        print(o)
        self.price = o['price']
        self.qty = o['qty']
        self.side = o['side']
        self.orderStatus = o['orderStatus']
        self.avgPrice = o['avgPrice']

    def __repr__(self) -> str:
        return f'''Лимитный ордер {self.side} 
        Кол-во: {self.qty} 
        Цена: {self.price}'''


class PositionInfo():
    def __init__(self, direction) -> None:
        self.positionIdx = direction[0]['positionIdx']
        self.symbol = direction[0]['symbol']
        self.side = direction[0]['side']
        self.size = direction[0]['size']
        self.avgPrice = direction[0]['avgPrice']
        self.positionValue = direction[0]['positionValue']
        self.markPrice = direction[0]['markPrice']
        self.bustPrice = direction[0]['bustPrice']
        self.takeProfit = direction[0]['takeProfit']
        self.cumRealisedPnl = direction[0]['cumRealisedPnl']

        self.limits = False
        self.limits_list = []
        if len(direction) >= 2:
            self.limits = True
            for o in direction[1:]:
                self.limits_list.append(LimitInfo(o))
        
    def __repr__(self) -> str:
        answer = f'''Позиция {SIDEBYIDX[self.positionIdx]} 
        Кол-во: {self.positionValue} 
        Средн. цена: {self.avgPrice} 
        TP: {self.takeProfit} 
        PnL: {self.cumRealisedPnl} 
        Цена ликвидации: {self.bustPrice}'''
        for o_inf in self.limits_list:
            answer += '\n' + str(o_inf)
        return answer + '\n'

class CoinInfo():
    def __init__(self, state) -> None:
        self.positions = []
        for direction in state:
            self.positions.append(PositionInfo(state[direction]))
    
    def __repr__(self) -> str:
        answer = f''
        for p_inf in self.positions:
            answer += '\n' + str(p_inf)
        return answer
      
class UserInfo():
    def __init__(self, testnet, api, secret, symbol):
        self.pairs = {}  # symbol: SmallPosition
        self.instr = Instruments(testnet, api, secret, symbol)

        self.symbol = symbol
        self.coin_info = None
        self.balance = 0
        self.apiStatus = None

    def update(self):
        try:
            self.coin_info = CoinInfo(self.instr.uber_info())
            self.apiStatus = True
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            self.apiStatus = False
            print('Api неверные')

    def __repr__(self) -> str:
        return f'{self.coin_info}'

    def monitoring(self):
        answer = ""
        for i in self.coin_control:
            if "Позиций: 0" not in str(self.coin_control[i]):
                answer += str(self.coin_control[i]) + '\n'
        return answer
        

