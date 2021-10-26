import numpy as np

from Utils import d1f, dN, N


def set_delta(flag, S, K, T, r, sigma):
    """ Black-Scholes-Merton Delta of European option. """
    d1 = d1f(S, K, T, r, sigma)

    if flag == 'p':
        return N(d1)-1  # put

    return N(d1)  # call


def set_gamma(S, K, T, r, sigma):
    """ Black-Scholes-Merton Gamma of European option. """
    d1 = d1f(S, K, T, r, sigma)
    return dN(d1) / (S * sigma * np.sqrt(T))


def set_theta(flag, S, K, T, r, sigma):
    """ Black-Scholes-Merton Theta of European option. """
    d1 = d1f(S, K, T, r, sigma)
    d2 = d1 - sigma * np.sqrt(T)

    if flag == 'p':
        return -(S * dN(d1) * sigma / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * N(-d2)  # put

    return -(S * dN(d1) * sigma / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * N(d2)  # call


def set_vega(S, K, T, r, sigma):
    """ Black-Scholes-Merton Vega of European option. """
    d1 = d1f(S, K, T, r, sigma)
    return S * dN(d1) * np.sqrt(T)


def set_rho(flag, S, K, T, r, sigma):
    """ Black-Scholes-Merton Rho of European option. """
    d1 = d1f(S, K, T, r, sigma)
    d2 = d1 - sigma * np.sqrt(T)

    if flag == 'p':
        return -K * T * np.exp(-r * T) * N(-d2)  # put

    return K * T * np.exp(-r * T) * N(d2)  # call


class Greeks:
    def __init__(self, flag, S, K, T, sigma, r):
        self.delta = set_delta(flag, S, K, T, r, sigma)
        self.gamma = set_gamma(S, K, T, r, sigma)
        self.theta = set_theta(flag, S, K, T, r, sigma)
        self.vega = set_vega(S, K, T, r, sigma)
        self.rho = set_rho(flag, S, K, T, r, sigma)
