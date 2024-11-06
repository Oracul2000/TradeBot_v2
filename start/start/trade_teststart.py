from strategies.test_strategy import Disptcher
from strategies.settings import StrategySettings

from multiprocessing import Process


sttngs = StrategySettings()

sttngs.api = 'mYt8OuTqfT2rdUAIJg'
sttngs.secret = 'XGhfPkMaTwpQf1UoPqV4XRRsrgltYnlPzOBd'
sttngs.testnet = True
sttngs.leverage = 20
sttngs.dep = 250
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
    0.2,
    0.4,
    0.8,
    1.6,
    3.2,
    6.4,
    12.8
]
sttngs.uid = 1
sttngs.logprefix = 'a/a.log'

dp = Disptcher(sttngs)
# dp.start()
# await dp.start()
# asyncio.run(dp.start())
def a():
    for i in range(100):
        print(2)

if __name__ == '__main__':
    p = Process(target=dp.start)