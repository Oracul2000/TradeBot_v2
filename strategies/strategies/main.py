from .classic_strategy import Disptcher
from .settings import StrategySettings


def startwrapper(sttngs: StrategySettings):
    dp = Disptcher(sttngs)
    dp.start()