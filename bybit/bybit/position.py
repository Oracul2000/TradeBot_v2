from .constants import *

import datetime

class Position:
    def __init__(self, data: dict) -> None:
        try:
            self.positionIdx = int(data['positionIdx'])
            self.symbol = data['symbol']
            self.side = data['side']

            self.entryPrice = 0
            if 'entryPrice' in data and data['entryPrice']:
                self.entryPrice = float(data['entryPrice'])
            elif 'avgPrice' in data and data['avgPrice']:
                self.entryPrice = float(data['avgPrice'])
            # if 'entryPrice' in data and data['entryPrice'] != '':
            #     self.entryPrice = float(data['entryPrice'])
            # if 'avgPrice' in data['avgPrice'] != '':
            #     self.entryPrice = float(data['avgPrice'])

            self.leverage = int(data['leverage'])

            self.positionValue = 0
            if data['positionValue'] != '':
                self.positionValue = float(data['positionValue'])

            # self.qty = self.positionValue * self.entryPrice
            self.markPrice = float(data['markPrice'])

            self.takeProfit = 0
            if data['takeProfit'] != '':
                self.takeProfit = float(data['takeProfit'])
                
            self.createdTime = data['createdTime']
            self.createdTimeReadable = datetime.datetime.utcfromtimestamp(int(self.createdTime) / 1e3)
            self.updatedTime = data['updatedTime']
            self.updatedTimeReadable = datetime.datetime.utcfromtimestamp(int(self.updatedTime) / 1e3)
            # self.positionStatus = data['positionStatus']        
        except BaseException as e:
            print(data)
            print(e)
            print("Error in Position init")

    def __repr__(self) -> str:
        return f'''
Symbol: {self.symbol}
Side: {self.side}
Entry Price: {self.entryPrice}
Position Idx: {self.positionIdx}
Take Profit: {self.takeProfit}
Created time: {self.createdTimeReadable}
Updated time: {self.updatedTimeReadable}
'''


# Posiotion value: {self.positionValue} ({self.qty} coins)$\tEntry Price: {self.entryPrice}
