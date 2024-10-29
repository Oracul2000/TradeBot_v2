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
        return resp
    
    def __position_info(self, positionIdx):
        positions = self.positions_info()
        for pos in positions['result']['list']:
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
        