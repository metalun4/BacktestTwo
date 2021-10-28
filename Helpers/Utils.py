import numpy as np

from scipy.integrate import quad


def dN(x):
    """ Probability density function of standard normal random variable x. """
    return np.exp(-0.5 * x ** 2) / np.sqrt(2 * np.pi)


def N(d):
    """ Cumulative density function of standard normal random variable x. """
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


def d1f(S, K, T, r, sigma):
    """ Black-Scholes-Merton d1 function. """
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))


def BSM_call_value(S, K, T, r, sigma):
    """ Calculates Black-Scholes-Merton European call option value. """
    d1 = d1f(S, K, T, r, sigma)
    d2 = d1 - sigma * np.sqrt(T)
    call_value = S * N(d1) - np.exp(-r * T) * K * N(d2)
    return call_value


def BSM_put_value(S, K, T, r, sigma):
    """ Calculates Black-Scholes-Merton European put option value. """
    return BSM_call_value(S, K, T, r, sigma) - S + np.exp(-r * T) * K
