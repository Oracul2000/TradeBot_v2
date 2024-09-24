from bybit.client import wsclient, wsclient_pybit


class Disptcher:
    def __init__(self) -> None:
        # wscl = wsclient('1IIDQovcA5ZYljlDTu', 'uwovHtsgA6dK3X8r6Y6dMB8Kn6jCCiqazsO0')
        wscl = wsclient_pybit('uk8aA70A45Td10DHfP', 'g6aKwkqfT1Bm810mSgw42Th8jfOZcd1tqeyf')
        wscl.test()
