import json
import time


class Msg:
    def __init__(self, type_msg, uid, symbol) -> None:
        self.type_msg = type_msg
        self.uid = uid
        self.symbol = symbol
        self.additional_text = ''
        
    def check(self, *params):
        pass

    def check_publish(self, *params):
        if self.check(*params):
            tgmsg = {
                'Type': self.type_msg,
                'User Id': self.uid,
                'symbol': self.symbol,
                'Additional': self.additional_text,
            }

            t = time.time()
            with open('bus/' + str(t), "w") as fp:
                json.dump(tgmsg, fp)


class OrderMsg(Msg):
    def __init__(self, aid, symbol) -> None:
        super().__init__("Order Message", aid, symbol)
        
    def check(self, order_number, condition_number):
        self.additional_text = f'Order number = {str(order_number)} >= {condition_number}'
        return order_number >= condition_number