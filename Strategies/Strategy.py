class Strategy:
    """ General strategy class for all. """
    def __init__(self, history, cash, dte):
        self.history = history
        self.cash = cash
        self.portfolio = [{'date': self.history.index[0], 'cash': cash}]
        self.dte = dte

        self.active_pos = None
        self._open = False

        self.T = dte/365
