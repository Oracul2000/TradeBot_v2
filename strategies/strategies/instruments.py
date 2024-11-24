from pybit.unified_trading import HTTP
import websockets

import time
import json
import hmac
import hashlib
import asyncio
import logging

from bybit.constants import *


class Instruments:
    def __init__(self, testnet, api, secret, symbol):
        self.symbol = symbol
        self.session = HTTP(
            testnet=testnet,
            api_key=api,
            api_secret=secret,
        )

    def positions_info(self):
        resp = self.session.get_positions(category="linear",
                                          symbol=self.symbol,
                                          )
        return resp['result']['list']

    def get_limit_orders(self):
        resp = self.session.get_open_orders(
            category='linear',
            symbol=self.symbol,
            openOnly=1,
            limit=1
        )
        return resp['result']['list']
    
    def get_balance(self):
        resp = self.session.get_wallet_balance(accountType='UNIFIED',
                                               coin='USDT')
        balance = 0
        if 'result' in resp and 'list' in resp['result']:
            balance = float(resp['result']['list'][0]['totalEquity'])
        return balance
    
    def get_statistics(self, start_time, stop_time):
        resp = self.session.get_closed_pnl(
            category='linear',
            symbol=self.symbol,
            startTime=start_time,
            stopTime=stop_time
        )
        if 'result' in resp and 'list' in resp['result']:
            return resp['result']['list']
    
    def get_info(self):
        sp = [0, 0, 0]
        positions = self.positions_info()
        for pos in positions:
            if pos['avgPrice'] and pos['avgPrice'] != '0':
                sp[0] += 1
            if pos['takeProfit']:
                sp[2] += 1

        limit_orders = self.get_limit_orders()
        for o in limit_orders:
            if o['symbol'] == self.symbol:
                sp[1] += 1
        return f'{sp[0]}{sp[1]}{sp[2]}'
    
    def uber_info(self):
        state = {LONGIDX: [], SHORTIDX: []}
        positions = self.positions_info()
        for pos in positions:
            posIdx = pos['positionIdx']
            state[posIdx].append(pos)
        
        limit_orders = self.get_limit_orders()
        for o in limit_orders:
            if o['symbol'] == self.symbol:
                oidx = o['positionIdx']
                state[oidx].append(o)

        return state
        
    
    def __position_info(self, positionIdx):
        positions = self.positions_info()
        for pos in positions:
            if int(pos['positionIdx']) == int(positionIdx):
                return pos
            
    def short_position_info(self):
        pos = self.__position_info(SIDEBYIDX['Sell'])
        return pos
    
    def long_positon_info(self):
        pos = self.__position_info(SIDEBYIDX['Buy'])
        return pos
    
    def position_size(self, positionIdx):
        pos = self.__position_info(positionIdx)
        if 'size' in pos:
            return float(pos['size'])

    def __close_position(self, positionIdx):
        qty = self.position_size(positionIdx)

        resp = self.session.place_order(
            category="linear",
            symbol=self.symbol,
            side=INVERSE_SIDEBYIDX[positionIdx],
            orderType="Market",
            qty=round(qty, roundationMap[self.symbol]),
            positionIdx=positionIdx
        )

    def close_short(self):
        self.__close_position(IDXBYSIDE['Sell'])


    def close_long(self):
        self.__close_position(IDXBYSIDE['Buy'])
        