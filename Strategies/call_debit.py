import pandas as pd

from Helpers.Option import Option
from Strategies.Strategy import Strategy


class CallDebit(Strategy):
    def open_position(self, curr_date, cost):
        self.portfolio += [{'date': curr_date, 'cash': self.portfolio[-1:][0]['cash'] - cost}]
        self._open += 1

    def close_position(self, curr_date, cost):
        self.portfolio += [{'date': curr_date, 'cash': self.portfolio[-1:][0]['cash'] + cost}]
        self._open = False

    def manage_position(self, x):
        # Manage short strangle position.
        rows = self.history.loc[x.index]
        row = rows.iloc[-1:]

        S = float(row['price'])
        r = .05
        sigma = float(row['implied_vol'] / 100)
        current_date = row.index[0]

        if self._open is False:
            # Calculate top and bottom strike prices based on returns
            top_K = int(S * (1 + row['return_mean'] + 0.5 * row['return_sd']))
            bot_K = int(S * (1 + row['return_mean'] - 2 * row['return_sd']))

            # Calculate position opening cost
            scall_premium = Option('c', S, top_K, self.T, r, sigma).price
            lcall_premium = Option('c', S, bot_K, self.T, r, sigma).price
            contract_cost = lcall_premium - scall_premium

            # Calculate multiplier (10% of portfolio)
            m = int((0.05 * self.portfolio[-1:][0]['cash']) / contract_cost)
            if m > 1:
                amount = m
            else:
                amount = 1

            self.open_position(current_date, contract_cost * amount)
            self.active_pos = {'scall': top_K, 'lcall': bot_K, 'cost': contract_cost, 'amount': amount}
        elif self._open <= self.dte:
            # Get current day to expiry
            T = (self.dte - self._open) / 365

            # Calculate position closing cost
            lcall_premium = Option('c', S, self.active_pos['lcall'], 0, r, sigma).price
            scall_premium = Option('c', S, self.active_pos['scall'], 0, r, sigma).price
            curr_cost = (lcall_premium - scall_premium) * self.active_pos['amount']

            # Opening cost
            cost = self.active_pos['cost'] * self.active_pos['amount']

            # always close at 125% of opening cost
            if curr_cost >= (125 / 100) * cost:
                self.close_position(current_date, curr_cost)
                self.active_pos = None
            else:
                self._open += 1

        else:
            # Calculate position closing cost
            lcall_premium = Option('c', S, self.active_pos['lcall'], 0, r, sigma).price
            scall_premium = Option('c', S, self.active_pos['scall'], 0, r, sigma).price
            cost = (lcall_premium - scall_premium) * self.active_pos['amount']

            self.close_position(current_date, cost)
            self.active_pos = None

        return 0

    def run_strategy(self):
        roll = self.history['price'].rolling(window=2)

        roll.apply(self.manage_position, raw=False)

        calculated_portfolio = pd.DataFrame(self.portfolio)
        calculated_portfolio.set_index('date', inplace=True)

        return calculated_portfolio
