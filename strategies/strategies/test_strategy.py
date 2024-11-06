import asyncio
from math import log

from bybit.client import wsclient_pybit
from bybit.constants import *
from .positions import *
from bybit.settings import *
from .messages import *
from .settings import StrategySettings


class Disptcher:
    def handle_position_stream(self, message):
        for i in message['data']:
            positionidx = i['positionIdx']
            positionValue = float(i['positionValue'])
            pos = self.positions[positionidx]

            if not pos.data:
                pos.data = i
                continue

            # Position is closed
            if positionValue == 0 and float(pos.data['positionValue']) != positionValue:
                self.positions[positionidx].cancelRecordedLimitOrders()                   

                self.positions[positionidx] = Position(self.wscl.session, positionidx, self.sttngs)
                self.steps[positionidx] = 0

                self.positions[positionidx].data = i
                price = float(self.wscl.session.get_kline(category="linear",
                                                    symbol=self.sttngs.symbol,
                                                    interval="1")['result']['list'][0][1])
                qty = self.calculate_value(positionidx, price)
                self.positions[positionidx].market_open(qty)
            else:
                self.positions[positionidx].data = i
                if self.steps[pos.positionIdx] == 6:
                    self.positions[positionidx].takeProfit(80)
                else:
                    self.positions[positionidx].takeProfit(10)

    def handle_execution_stream(self, message):
        pass
        
    def handle_order_stream(self, message):
        for i in message['data']:
            orderId_callback = i['orderId']
            orderStatus_callback = i['orderStatus']
            positionIdx_callback = i['positionIdx']

            pos = self.positions[positionIdx_callback]

            # Market Order is Filled
            if orderId_callback in pos.markets:
                order = pos.markets[orderId_callback]
                assert type(order) is Order
                order.isFilled(i)
                if order.status == ORDERFILLED:
                    price = self.calculate_price(pos.positionIdx, float(order.data['avgPrice']))
                    qty = self.calculate_value(pos.positionIdx, price)
                    pos.limit_open(qty, price)

            # Limit order is Filled
            elif orderId_callback in pos.limits:
                order = pos.limits[orderId_callback]
                assert type(order) is Order
                order.isFilled(i)
                if order.status == ORDERFILLED:
                    self.orderMsg.check_publish(self.steps[pos.positionIdx] + 2, 7)

                    self.create_limit(pos, float(order.data['avgPrice']))

    def create_limit(self, pos: Position, start_price):
        if self.steps[pos.positionIdx] == 6:
            pass
        else:
            self.steps[pos.positionIdx] += 1
            price = self.calculate_price(pos.positionIdx, start_price)
            qty = self.calculate_value(pos.positionIdx, price)
            pos.limit_open(qty, price)

    def __create_bybit_settings(self, sttngs: StrategySettings) -> ByBitSettings:
        bbs = ByBitSettings()
        bbs.testnet = sttngs.testnet
        bbs.symbol = sttngs.symbol
        bbs.api = sttngs.api
        bbs.secret = sttngs.secret
        bbs.logprefix = sttngs.logprefix
        bbs.leverage = sttngs.leverage
        return bbs

    def __init__(self, sttngs: StrategySettings) -> None:
        self.sttngs = sttngs
        self.wscl = wsclient_pybit(self.__create_bybit_settings(sttngs))

        self.positions = {LONGIDX: Position(self.wscl.session, LONGIDX, self.sttngs),
                          SHORTIDX: Position(self.wscl.session, SHORTIDX, self.sttngs)}
        self.steps = {LONGIDX: 0,
                      SHORTIDX: 0}
        
        self.orderMsg = OrderMsg(self.sttngs.uid, self.sttngs.symbol) 

    def calculate_value(self, positionIdx: int, price_at_moment: float):
        step = self.steps[positionIdx]
        percents_from_dep = self.sttngs.valuemap[step + 1]
        value_in_usdt = self.sttngs.dep * percents_from_dep / 100
        value_in_coins = value_in_usdt / price_at_moment * self.sttngs.leverage
        return value_in_coins
    
    def calculate_price(self, positionIdx: int, start_price: float):
        step = self.steps[positionIdx]
        percents_from_start_price = self.sttngs.stepmap[step]
        operator = {LONGIDX: -1, SHORTIDX: 1}[positionIdx]
        price = start_price * (1 + operator * percents_from_start_price / 100)
        return price

    def start(self):
        try:
            self.wscl.session.switch_position_mode(category='linear',
                                                symbol=self.sttngs.symbol,
                                                mode=3)
        except Exception:
            pass
        for positionidx, pos in self.positions.items():
            pos.self_update()
            price = float(self.wscl.session.get_kline(category="linear",
                                                symbol=self.sttngs.symbol,
                                                interval="1")['result']['list'][0][1])
            if pos.data['avgPrice'] == '0':
                qty = self.calculate_value(positionidx, price)
                self.wscl.set_prestart(pos.market_open, qty)
            else:
                start_qty = self.sttngs.dep * self.sttngs.valuemap[1]
                start_value_usdt = start_qty * price
                ratio = float(pos.data['positionValue']) / start_value_usdt
                step = round(log(ratio, 2), 0) - 1
                self.steps[pos.positionIdx] = int(step)
                self.wscl.set_prestart(self.create_limit, pos, price)
            pos.data = {}
        time.sleep(2)
        asyncio.run(self.wscl.bind(self.handle_position_stream, self.handle_execution_stream, self.handle_order_stream))
    