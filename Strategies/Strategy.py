class Strategy:
    """ General strategy class for all. """
    def __init__(self, history, portfolio, dte):
        self.history = history
        self.portfolio = portfolio
        self.dte = dte

        self.T = dte/365
