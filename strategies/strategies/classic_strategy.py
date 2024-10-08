from bybit.client import wsclient_pybit
from bybit.position import Position
from bybit.position_trade_wrapper import PositionTradeWrapper
from bybit.execution import Execution
from bybit.order import LimitOrder
from bybit.settings import ByBitSettings
from bybit.constants import *
from .settings import StrategySettings


class Disptcher:
    def handle_position_stream(self, message):
        print(4.1)
        for i in message['data']:
            pos = Position(i)
            if pos.symbol != self.sttngs.symbol:
                print('Not this symbol')
                continue
            ptw = self.ptws[pos.positionIdx]
            step = self.steps[pos.positionIdx]
            start_price = self.start_prices[pos.positionIdx]


            if pos.positionValue == 0:
                print('\t\tPosition is closed')
                ptw.self_update()
                if ptw.pos.positionValue == 0:
                    qty = self.calculate_value(ptw.pos.positionIdx, ptw.pos.markPrice)
                    ptw.market_open(qty, ptw.pos.positionIdx)
                    step = 0
                    start_price = 0
                    print(1, self.start_prices)
            
            if ptw.pos.positionValue == 0 and pos.positionValue != 0:
                print('\t\tMarket Order Opened Event')
                ptw.self_update()
                if ptw.pos.positionValue != 0:
                    step = 0
                    start_price = pos.entryPrice
                    print(2, self.start_prices)

                    price = self.calculate_price(pos.positionIdx, start_price)
                    qty = self.calculate_value(pos.positionIdx, price)
                    ptw.limit_open(qty, pos.positionIdx, price)
                    ptw.takeProfit(400)
        print()

    def handle_execution_stream(self, message):
        return
        print(4.2)
        print(message)
        return
        
    def handle_order_stream(self, message):
        print(4.3)
        for i in message['data']:
            lo = LimitOrder(i)
            ptw = self.ptws[lo.positionIdx]
            step = self.steps[lo.positionIdx]
            if lo.orderId in ptw.limits:
                print("Limit Order Filled")
                step += 1
                del ptw.limits[lo.orderId]

                start_price = self.start_prices[ptw.positionIdx]
                print(3, self.start_prices)
                price = self.calculate_price(ptw.positionIdx, start_price)
                qty = self.calculate_value(ptw.positionIdx, price)
                ptw.limit_open(qty, ptw.positionIdx, price)
                ptw.takeProfit(400)
        return

    def __create_bybit_settings(self, sttngs: StrategySettings) -> ByBitSettings:
        bbs = ByBitSettings()
        bbs.testnet = sttngs.testnet
        bbs.symbol = sttngs.symbol
        bbs.api = sttngs.api
        bbs.secret = sttngs.secret
        bbs.logprefix = ''
        bbs.leverage = sttngs.leverage
        return bbs

    def __init__(self, sttngs: StrategySettings) -> None:
        self.sttngs = sttngs
        self.wscl = wsclient_pybit(self.__create_bybit_settings(sttngs))

        self.positions = {}
        self.ptws = {LONGIDX: PositionTradeWrapper(self.wscl.session, self.wscl.bbs, LONGIDX),
                     SHORTIDX: PositionTradeWrapper(self.wscl.session, self.wscl.bbs, SHORTIDX)}
        self.steps = {LONGIDX: 0,
                      SHORTIDX: 0}
        self.start_prices = {LONGIDX: 0,
                             SHORTIDX: 0}
        
    def calculate_value(self, positionIdx: int, price_at_moment: float):
        ptw = self.ptws[positionIdx]
        step = self.steps[positionIdx]
        percents_from_dep = self.sttngs.valuemap[step + 1]
        value_in_usdt = self.sttngs.dep * percents_from_dep / 100
        value_in_coins = value_in_usdt / price_at_moment * ptw.bbs.leverage
        return value_in_coins
    
    def calculate_price(self, positionIdx: int, start_price: float):
        ptw = self.ptws[positionIdx]
        step = self.steps[positionIdx]
        percents_from_start_price = self.sttngs.stepmap[step]
        operator = {LONGIDX: -1, SHORTIDX: 1}[positionIdx]
        price = start_price * (1 + operator * percents_from_start_price / 100)
        return price

    def start(self):
        for positionIdx, ptw in self.ptws.items():
            ptw.self_update()
            qty = self.calculate_value(positionIdx, ptw.pos.markPrice)
            ptw.market_open(qty, positionIdx)
        
        self.wscl.bind(self.handle_position_stream, self.handle_execution_stream, self.handle_order_stream)