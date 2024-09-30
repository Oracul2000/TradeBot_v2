import datetime

class Execution:
    def __init__(self, data: dict) -> None:
        self.symbol = data['symbol']
        self.closedSize = data['closedSize']
        self.execPrice = data['execPrice']
        self.execQty = data['execQty']
        self.execType = data['execType']
        self.execValue = data['execValue']
        self.orderPrice = data['orderPrice']
        self.orderQty = data['orderQty']
        self.orderType = data['orderType']
        self.stopOrderType = data['stopOrderType']
        self.side = data['side']
        self.execTime = data['execTime']
        self.execTimeReadable = datetime.datetime.utcfromtimestamp(int(self.execTime) / 1e3)
        self.closedPnl = data['closedPnl']


    def __repr__(self) -> str:
        s = 'Execution:\n'
        attrs = vars(self)
        for i in attrs:
            s += f'{i}: {attrs[i]}\n'
        return s