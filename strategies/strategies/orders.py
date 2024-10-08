from .constants import *


class Order:
    def __init__(self) -> None:
        self.status = ORDERINITED

        self.data = {}

    def isSended(self, data: dict):
        self.orderId = data['orderId']
        self.status = ORDERSENDED
        print(f'Order {self.orderId} is Sended')

    def isFilled(self, data: dict):
        self.data = data
        if data['orderStatus'] == 'Filled':
            self.status = ORDERFILLED
            print(f'Order {self.orderId} is Filled')
    