from pybit.unified_trading import WebSocket
import websockets

import time
import json
import hmac
import hashlib
import asyncio
import logging

from .constants import *
from .config import *
from .errors import *
from .position import Position


class wsclient:
    # Constants
    testnet_urls = {
        PerpetualStream: "wss://stream-testnet.bybit.com/v5/public/linear",
        PrivateStream: "wss://stream-testnet.bybit.com/v5/private",
        OrderEntryStream: "wss://stream-testnet.bybit.com/v5/trade"
    }

    def __init__(self, api: str, secret: str) -> None:
        self.api = api
        self.secret = secret
        asyncio.get_event_loop().run_until_complete(self.auth())

    def gen_signature(self, payload, timeStamp, apiKey, secretKey, recvWindow):
        param_str = str(timeStamp) + apiKey + recvWindow + payload
        hash = hmac.new(bytes(secretKey, "utf-8"),
                        param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature
    
    async def __send__(self, op: str, params: list, websocket: websockets.WebSocketClientProtocol):
        await websocket.send(json.dumps({"op": op,
                                  "args": params}))
        response = json.loads(await websocket.recv())
        return response
    
    async def __send2__(self, topic: str, websocket: websockets.WebSocketClientProtocol):
        await websocket.send(json.dumps({"topic": topic}))
        response = json.loads(await websocket.recv())
        return response


    async def auth(self):
        logging.info('Start of auth')
        expires = int((time.time() + 1) * 10000)
        signature = str(hmac.new(bytes(self.secret, "utf-8"),
                                 bytes(f"GET/realtime{expires}", "utf-8"),
                                 digestmod="sha256").hexdigest())

        async with websockets.connect(self.testnet_urls[PrivateStream]) as websocket:
            # await websocket.send(json.dumps({
            #     "op": "auth",
            #     "args": [self.api, expires, signature]
            # })
            # )
            # response = json.loads(await websocket.recv())
            response = await self.__send__(op='auth', 
                                           params=[self.api, expires, signature], 
                                           websocket=websocket)
            logging.info(response)
            if not response["success"]:
                raise AuthError()
            print(f"Received: {response}")
            response = await self.__send2__("kline.30.BTCUSDT", websocket)
            print(response)


class wsclient_pybit:
    def __init__(self, api: str, secret: str):
        self.wsprivate = WebSocket(
            testnet=True,
            channel_type="private",
            api_key=api,
            api_secret=secret,
            # trace_logging=True
            # restart_on_error=True,
        )
        self.api = api
        self.secret = secret


    def test(self):
        def position_stream_handle(message):
            pos1, pos2 = [Position(i) for i in message['data']]
            print(pos1)
            print(pos2)
            print()

        self.wsprivate.position_stream(callback=position_stream_handle)
        while True:
            time.sleep(1)
