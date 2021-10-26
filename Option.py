# from Greeks import Greeks
from Utils import BSM_call_value, BSM_put_value


class Option:
    def __init__(self, flag, S, K, T, r, sigma):
        if flag == 'c':
            self.price = BSM_call_value(S, K, T, r, sigma)
        else:
            self.price = BSM_put_value(S, K, T, r, sigma)

        # Don't need to calc greeks for now
        # self.greeks = Greeks(flag, S, K, T, r, sigma)
