import logging

from .classic_strategy import Disptcher
from .settings import StrategySettings


def startwrapper(sttngs: StrategySettings):
    while True:
        dp = Disptcher(sttngs)
        dp.start()
        logging.error("loop is ended")
