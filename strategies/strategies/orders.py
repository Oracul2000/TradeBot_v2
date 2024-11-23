from .constants import *
import logging


class Order:
    def __init__(self) -> None:
        self.status = ORDERINITED

        self.data = {}

    def isSended(self, data: dict):
        self.orderId = data['orderId']
        self.status = ORDERSENDED
        logging.info(f'Order {self.orderId} is Sended\nData:{data}')

    def isFilled(self, data: dict):
        self.data = data
        if data['orderStatus'] == 'Filled':
            self.status = ORDERFILLED
            logging.info(f'Order {self.orderId} is Filled\nData:{data}')
    