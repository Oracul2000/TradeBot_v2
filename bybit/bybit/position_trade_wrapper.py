from .constants import *
from .position import *
from .order import *
from .settings import *

from pybit.unified_trading import HTTP


class PositionTradeWrapper:
    def __init__(self, session: HTTP, bbs: ByBitSettings, positionIdx: int, step: int=0):
        self.session = session
        self.bbs = bbs
        self.step = step
        self.positionIdx = positionIdx
        self.roundation = 0
        self.start_price = None

    def positionselfupd(self):
        tradepositions = self.session.get_positions(category="linear", symbol=self.bbs.symbol)["result"]["list"]
        for i in tradepositions:
            if i['positionIdx'] == self.positionIdx:
                self.pos = Position(i)
        if not self.pos:
            print('No position')
        if self.step == 0:
            self.start_price = float(self.pos.entryPrice)

    def positionforceupd(self, data):
        self.pos = Position(data)
        if self.step == 0:
            self.start_price = float(self.pos.entryPrice)

    def takeProfit(self, percents):
        takeProfitPrice = None
        if self.pos.positionIdx == LONGIDX:
            takeProfitPrice = self.pos.entryPrice * (1 + percents / 100 / self.bbs.leverage)
        else:
            takeProfitPrice = self.pos.entryPrice * (1 - percents / 100 / self.bbs.leverage)

        self.session.set_trading_stop(
            category="linear",
            symbol=self.pos.symbol,
            takeProfit=str(round(takeProfitPrice, 5)),
            tpTriggerBy="MarkPrice",
            tpslMode="Full",
            tpOrderType="Market",
            positionIdx=self.pos.positionIdx
        )

    def open(self, qty, positionIdx):
        self.session.place_order(
            category="linear",
            symbol=self.bbs.symbol,
            side=SIDEBYIDX[positionIdx],
            orderType="Market",
            qty=round(qty, self.roundation),
            positionIdx=positionIdx
        )

    def limitopen(self, qty, positionIdx, price):
        self.session.place_order(
            category="linear",
            symbol=self.bbs.symbol,
            side=SIDEBYIDX[positionIdx],
            orderType="Limit",
            qty=self.roundation(qty),
            positionIdx=positionIdx,
            price=price
        )

    def closed_event(self):
        self.step = 0
        # self.open(100, self.pos.positionIdx)

    def changed_event(self):
        self.takeProfit(400)

