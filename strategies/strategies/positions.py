from pybit.unified_trading import HTTP

from .constants import *
from .orders import *
from .settings import *


class Position:
    def __init__(self, session: HTTP, positionIdx: int, sttngs: StrategySettings) -> None:
        self.session = session
        self.positionIdx = positionIdx
        self.sttngs = sttngs
        
        self.limits = {}
        self.markets = {}
        self.tps = {}

        self.roundation = 0
        self.start_price = 0
        self.data = {}

    def market_open(self, qty):
        order = Order()

        resp = self.session.place_order(
            category="linear",
            symbol=self.sttngs.symbol,
            side=SIDEBYIDX[self.positionIdx],
            orderType="Market",
            qty=round(qty, self.roundation),
            positionIdx=self.positionIdx
        )
        
        order.isSended(resp['result'])
        self.markets[order.orderId] = order

    def self_update(self):
        tradepositions = self.session.get_positions(category="linear", symbol=self.sttngs.symbol)["result"]["list"]
        for i in tradepositions:
            if i['positionIdx'] == self.positionIdx:
                self.data = i

    def limit_open(self, qty, price):
        order = Order()

        resp = self.session.place_order(
            category="linear",
            symbol=self.sttngs.symbol,
            side=SIDEBYIDX[self.positionIdx],
            orderType="Limit",
            qty=round(qty, self.roundation),
            positionIdx=self.positionIdx,
            price=price
        )
        order.isSended(resp['result'])
        self.limits[order.orderId] = order

    def takeProfit(self, percents):
        self.self_update()
        entry_price = float(self.data['avgPrice'])
        takeProfitPrice = None
        if self.positionIdx == LONGIDX:
            takeProfitPrice = entry_price * (1 + percents / 100 / self.sttngs.leverage)
        else:
            takeProfitPrice = entry_price * (1 - percents / 100 / self.sttngs.leverage)

        self.session.set_trading_stop(
            category="linear",
            symbol=self.sttngs.symbol,
            takeProfit=str(round(takeProfitPrice, 5)),
            tpTriggerBy="MarkPrice",
            tpslMode="Full",
            tpOrderType="Market",
            positionIdx=self.positionIdx
        )

