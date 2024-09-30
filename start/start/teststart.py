from strategies.classic_strategy import Disptcher
from strategies.settings import StrategySettings

sttngs = StrategySettings()

sttngs.api = '1IIDQovcA5ZYljlDTu'
sttngs.secret = 'uwovHtsgA6dK3X8r6Y6dMB8Kn6jCCiqazsO0'
sttngs.testnet = True
sttngs.leverage = 20
sttngs.dep = 150
sttngs.stepmap = [
    0.3,
    0.8,
    1.8,
    3.2,
    6,
    10,
    15
]
sttngs.symbol = 'DOGEUSDT'
sttngs.valuemap = [
    0.2,
    0.4,
    0.8,
    1.6,
    3.2,
    6.4,
    12.8
]

dp = Disptcher(sttngs)
dp.start()
