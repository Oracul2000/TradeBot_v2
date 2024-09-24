import datetime

class Position:
    def __init__(self, data: dict) -> None:
        self.positionIdx = data['positionIdx']
        self.symbol = data['symbol']
        self.side = data['side']
        self.entryPrice = data['entryPrice']
        self.leverage = data['leverage']
        self.positionValue = data['positionValue']
        self.markPrice = data['markPrice']
        self.positionIM = data['positionIM']
        self.positionMM = data['positionMM']
        self.takeProfit = data['takeProfit']
        self.unrealisedPnl = data['unrealisedPnl']
        self.cumRealisedPnl = data['cumRealisedPnl']
        self.createdTime = data['createdTime']
        self.createdTimeReadable = datetime.datetime.utcfromtimestamp(int(self.createdTime) / 1e3)
        self.updatedTime = data['updatedTime']
        self.updatedTimeReadable = datetime.datetime.utcfromtimestamp(int(self.updatedTime) / 1e3)
        self.positionStatus = data['positionStatus']

    def __repr__(self) -> str:
        return f'''
Symbol: {self.symbol}
Side: {self.side}
Position Idx: {self.positionIdx}
Posiotn value: {self.positionValue}
Position status: {self.positionStatus}
Created time: {self.createdTimeReadable}
Updated time: {self.updatedTimeReadable}
'''

