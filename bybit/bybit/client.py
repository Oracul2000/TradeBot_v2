from pybit.unified_trading import WebSocket
from pybit.unified_trading import HTTP
import websockets

import time
import json
import hmac
import hashlib
import asyncio
import logging

from .constants import *
from .errors import *
from .position import Position
from .execution import Execution
from .order import LimitOrder
from .settings import ByBitSettings


class wsclient_pybit:
    # def __init__(self, api: str, secret: str):
    def __init__(self, bbs: ByBitSettings):
        self.wsprivate = WebSocket(
            testnet=bbs.testnet,
            channel_type="private",
            api_key=bbs.api,
            api_secret=bbs.secret,
            trace_logging=True
            # restart_on_error=True,
        )

        self.session = HTTP(
            testnet=bbs.testnet,
            api_key=bbs.api,
            api_secret=bbs.secret,
        )

        self.ws = WebSocket(
            testnet=bbs.testnet,
            channel_type="linear",
        )

        self.session = HTTP(
            testnet=bbs.testnet,
            api_key=bbs.api,
            api_secret=bbs.secret,
        )

        self.bbs = bbs

        # self.market_order = lambda side, qty: self.session.place_order(
        #     category="linear",
        #     symbol=bbs.symbol,
        #     side=side,
        #     orderType="Market",
        #     qty=qty
        # )

    def switch_position_mode(self):
        self.session.switch_position_mode(
            category="linear",
            symbol=self.bbs.symbol,
            mode=3
        )

    def bind(self, handle_position_stream, 
             handle_execution_stream,
             handle_order_stream):
        self.wsprivate.position_stream(handle_position_stream)
        # self.wsprivate.execution_stream(handle_execution_stream)
        # self.wsprivate.order_stream(handle_order_stream)
        while True:
            time.sleep(0.1)
            