import datetime

class LimitOrder:
    def __init__(self, data: dict) -> None:
        self.symbol = data['symbol']
        self.orderId = data['orderId']
        self.side = data['side']
        self.positionIdx = data['positionIdx']
        self.orderStatus = data['orderStatus']
        self.cancelType = data['cancelType']
        self.rejectReason = data['rejectReason']
        self.price = data['price']
        self.qty = data['qty']
        self.avgPrice = data['avgPrice']
        self.orderType = data['orderType']
        self.createdTime = data['createdTime']
        self.createdTimeReadable = datetime.datetime.utcfromtimestamp(int(self.createdTime) / 1e3)
        self.updatedTime = data['updatedTime']
        self.updatedTimeReadable = datetime.datetime.utcfromtimestamp(int(self.updatedTime) / 1e3)
        self.createType = data['createType']

    def __repr__(self) -> str:
        s = 'Order:\n'
        attrs = vars(self)
        for i in attrs:
            s += f'{i}: {attrs[i]}\n'
        return s
    
    def __eq__(self, other) -> bool:
        return self.orderId == other.orderId