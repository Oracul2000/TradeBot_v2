import websockets

from pybit.unified_trading import HTTP

import time
import json
import hmac
import hashlib
import asyncio
import logging

from .constants import *
from .errors import *
from .settings import ByBitSettings


class wsclient:
    # Constants
    testnet_urls = {
        PerpetualStream: "wss://stream-testnet.bybit.com/v5/public/linear",
        PrivateStream: "wss://stream-testnet.bybit.com/v5/private",
        OrderEntryStream: "wss://stream-testnet.bybit.com/v5/trade"
    }

    mainnet_urls = {
        PerpetualStream: "wss://stream.bybit.com/v5/public/linear",
        PrivateStream: "wss://stream.bybit.com/v5/private",
        OrderEntryStream: "wss://stream.bybit.com/v5/trade"
    }

    urls = {
        True: testnet_urls,
        False: mainnet_urls
    }

    def __init__(self, bbs) -> None:
        self.prestart_funcs = []
        self.prestart_args = []

        self.bbs = bbs

        self.session = HTTP(
            testnet=bbs.testnet,
            api_key=bbs.api,
            api_secret=bbs.secret,
        )

    def gen_signature(self, payload, timeStamp, apiKey, secretKey, recvWindow):
        param_str = str(timeStamp) + apiKey + recvWindow + payload
        hash = hmac.new(bytes(secretKey, "utf-8"),
                        param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature
    
    def bind(self, handle_position_stream, handle_order_stream):
        self.handle_position_stream = handle_position_stream
        self.handle_order_stream = handle_order_stream
    
    async def __send(self, op: str, params: list, websocket: websockets.WebSocketClientProtocol):
        print(json.dumps({"op": op,
                                  "args": params}))
        await websocket.send(json.dumps({"op": op,
                                  "args": params}))
        response = json.loads(await websocket.recv())
        print(response)
        return response
    
    async def __subscribe(self, websocket: websockets.WebSocketClientProtocol):
        await websocket.send(json.dumps({"op": "subscribe",
                                         "args": ["position.linear"]}))
        await websocket.send(json.dumps({"op": "subscribe",
                                         "args": ["order"]}))
        response = json.loads(await websocket.recv())
        return response
    
    def start_wrapper(self):
        logging.info("self_written_client - wsclient - def start_wrapper")
        asyncio.get_event_loop().run_until_complete(self.start())

    async def start(self):
        expires = int((time.time() + 1) * 10000)
        signature = str(hmac.new(bytes(self.bbs.secret, "utf-8"),
                                 bytes(f"GET/realtime{expires}", "utf-8"),
                                 digestmod="sha256").hexdigest())

        async with websockets.connect(self.testnet_urls[PrivateStream]) as websocket:
            response = await self.__send(op='auth', 
                                        params=[self.bbs.api, expires, signature], 
                                        websocket=websocket)
            if not response["success"]:
                raise AuthError()
            response = await self.__subscribe(websocket)

            not_started = True
            while True:
                if not_started:
                    await self.async_prestart()
                    not_started = False
                data = json.loads(await websocket.recv())
                if 'topic' not in data:
                    continue
                if data['topic'] == 'position.linear':
                    self.handle_position_stream(data)
                if data['topic'] == 'order':
                    self.handle_order_stream(data)

    def switch_position_mode(self):
        self.session.switch_position_mode(
            category="linear",
            symbol=self.bbs.symbol,
            mode=3)

    def set_prestart(self, func, *args):
        self.prestart_funcs.append(func)
        self.prestart_args.append(args)

    async def async_prestart(self):
        for f, x in zip(self.prestart_funcs, self.prestart_args):
            f(*x)

