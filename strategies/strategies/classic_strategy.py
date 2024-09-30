from bybit.client import wsclient_pybit
from bybit.position import Position
from bybit.position_trade_wrapper import PositionTradeWrapper
from bybit.execution import Execution
from bybit.settings import ByBitSettings
from bybit.constants import *
from .settings import StrategySettings


class Disptcher:
    def handle_position_stream(self, message):
        print(4.1)
        for i in message['data']:
            pos = Position(i)
            print(pos)
            if pos.symbol != self.sttngs.symbol:
                print('Not this symbol')
                continue
            if self.ptws[pos.positionIdx].pos.entryPrice != pos.entryPrice and pos.entryPrice != 0:
                self.ptws[pos.positionIdx].pos = pos
                self.ptws[pos.positionIdx].changed_event()
            self.ptws[pos.positionIdx].pos = pos
            if pos.positionValue == 0:
                self.ptws[pos.positionIdx].closed_event()
                qty = self.determine_value(self.ptws[pos.positionIdx], pos.markPrice)
                self.ptws[pos.positionIdx].open(qty, pos.positionIdx)
        print()

    def handle_execution_stream(self, message):
        return
        
    def handle_order_stream(self, message):
        print(message)

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
    
    def determine_price(self, ptw: PositionTradeWrapper):
        operation = -1
        if ptw.positionIdx == SHORTIDX:
            operation = 1
        price = ptw.start_price * (1 + operation * self.sttngs.stepmap[ptw.step + 1] / 100)
        return price
    
    def determine_value(self, ptw: PositionTradeWrapper, price):
        # price = self.determine_price(ptw)
        percents = self.sttngs.valuemap[ptw.step + 1]
        usdt_price = self.sttngs.dep * percents / 100 * ptw.bbs.leverage
        print(price)
        return usdt_price / price



    def start(self):
        for _, ptw in self.ptws.items():
            ptw.positionselfupd()
            qty = self.determine_value(ptw, ptw.pos.markPrice)
            ptw.open(qty, ptw.pos.positionIdx)
            print(ptw.pos)
        
        self.wscl.bind(self.handle_position_stream, self.handle_execution_stream, self.handle_order_stream)