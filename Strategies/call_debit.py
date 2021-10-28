import pandas as pd

from Helpers.Option import Option
from Strategy import Strategy


class CallDebit(Strategy):
    def __init__(self, history, portfolio, dte):
        super().__init__(history, portfolio, dte)
        self.active_pos = None
        self._open = False
