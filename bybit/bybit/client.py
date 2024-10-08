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
from .settings import ByBitSettings


class wsclient_pybit:
    def __init__(self, bbs: ByBitSettings):
        self.prestart_funcs = []
        self.prestart_args = []

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

    def switch_position_mode(self):
        self.session.switch_position_mode(
            category="linear",
            symbol=self.bbs.symbol,
            mode=3
        )

    def set_prestart(self, func, *args):
        self.prestart_funcs.append(func)
        self.prestart_args.append(args)

    async def async_prestart(self):
        for f, x in zip(self.prestart_funcs, self.prestart_args):
            f(*x)

    async def bind(self, handle_position_stream, 
             handle_execution_stream,
             handle_order_stream):
        self.wsprivate.position_stream(handle_position_stream)
        self.wsprivate.execution_stream(handle_execution_stream)
        self.wsprivate.order_stream(handle_order_stream)

        not_started = True
        while True:
            if not_started:
                await self.async_prestart()
                not_started = False
                time.sleep(2)
            time.sleep(0.01)
            