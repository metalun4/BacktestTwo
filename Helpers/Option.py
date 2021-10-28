# from Greeks import Greeks
from Helpers.Utils import BSM_call_value, BSM_put_value


class Option:
    def __init__(self, flag, S, K, T, r, sigma):
        if flag == 'c':
            self.price = float(BSM_call_value(S, K, T, r, sigma))
        else:
            self.price = float(BSM_put_value(S, K, T, r, sigma))

        # Don't need to calc greeks for now
        # self.greeks = Greeks(flag, S, K, T, r, sigma)
