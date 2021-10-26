import numpy as np
import pandas as pd
import matplotlib as mpl

from Strategy import ShortStrangle

mpl.rcParams['font.family'] = 'serif'


class Backtester(object):

    def __init__(self, initial_deposit, symbol, start, end, data=None):
        self.initial_deposit = initial_deposit
        self.cash = initial_deposit
        self.symbol = symbol
        self.start = start
        self.end = end
        if data is None:
            self.data, self.calculated_data = self.get_sample_data()
        else:
            self.data = data

    def get_sample_data(self):
        file = pd.read_csv('sample_data.csv', index_col=0, parse_dates=True).dropna()

        # Get ticker history
        ticker_history = pd.DataFrame(file[self.symbol])
        ticker_history.rename(columns={self.symbol: 'price'}, inplace=True)

        # Get volatility index history
        vix_history = pd.DataFrame(file['.VIX'])
        vix_history.rename(columns={'.VIX': 'implied_vol'}, inplace=True)

        history = pd.merge(ticker_history, vix_history, how='left', left_index=True, right_index=True)
        raw_history = history.loc[self.start:self.end]

        # Calculate price returns.
        history['return'] = np.log(history['price'] / history['price'].shift(1))
        history['realized_vol'] = history['return'].rolling(21).std() * np.sqrt(252) * 100
        history['actual_return'] = history['price'].pct_change(45)
        history['return_sd'] = history['actual_return'].rolling(45).std()
        history['return_mean'] = history['actual_return'].rolling(45).mean()
        history.dropna(inplace=True)

        return raw_history, history

    def main(self):
        portfolio = [{'date': self.calculated_data.index[0], 'cash': self.initial_deposit}]

        strat = ShortStrangle(self.calculated_data, portfolio, 30)

        tested = strat.run_strategy()

        tested['cash'].plot(title="portfolio size")

        print("Portfolio current value: $%.2f" %tested.iloc[-1]['cash'])
