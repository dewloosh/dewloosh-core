# -*- coding: utf-8 -*-
import time
import sys
from dewloosh.core.tools.typing import issequence
import numpy as np


def floatformatter(*args, sig=6, **kwargs):
    return "{" + "0:.{}g".format(sig) + "}"


def float_to_str_sig(value, *args, sig: int = 6, atol: float = 1e-7, **kwargs):
    """
    Returns a string representation of a floating point number, with
    given significant digits.

    Parameters
    ----------
    value : float or a sequence of floats
        A single value, or an iterable.

    sig : int
        Number of significant digits.

    atol : float
        Floating point tolerance. Values smaller than this are 
        considered to be zero.

    Returns
    -------
    string or a sequence of strings
        String representation of the provided input.
    """
    if not issequence(value):
        if atol is not None:
            if abs(value) < atol:
                value = 0.0
        return '{:.{p}g}'.format(value, p=sig)
    else:
        value = np.array(value)
        if atol is not None:
            inds = np.where(np.abs(value) < atol)[0]
            value[inds] = 0.0
        formatter = floatformatter(sig=sig)
        def f(v): return formatter.format(v)
        return list(map(f, value))


def timer(fnc):
    def inner(*args, **kwargs):
        t0 = time.time()
        fnc(*args, **kwargs)
        t1 = time.time()
        return t1-t0
    return inner


def SuppressedFunction(fnc):
    """Decorator that wraps a function to suppress 
    it's calls to print()"""
    def inner(*arg):
        original_stdout = sys.stdout
        sys.stdout = None
        res = fnc(*arg)
        sys.stdout = original_stdout
        return res
    return inner


def alphabet(abctype: str = 'latin', **kwargs):
    if abctype in ('ord', 'o'):
        start = kwargs.pop('start', 0)
    elif abctype in ('latin', 'l'):
        start = ord(kwargs.pop('start', 'a'))
    elif abctype == 'u':
        start = ord(kwargs.pop('start', '\u0000'))
    elif abctype in ('greek', 'g'):
        start = ord(kwargs.pop('start', '\u03b1'))
    while True:
        yield chr(start)
        start += 1


def ordrange(N: int = 1, **kwargs):
    start = kwargs.pop('start', 0)
    if isinstance(start, str):
        start = ord(start)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [chr(c) for c in range(start, stop)]


def latinrange(N: int = 1, **kwargs):
    start = kwargs.pop('start', 97)
    stop = kwargs.pop('stop', None)
    return ordrange(N, start=start, stop=stop)


def urange(N: int = 1, **kwargs):
    start = kwargs.pop('start', '\u0000')
    stop = kwargs.pop('stop', None)
    if stop is None:
        stop = start
    return ordrange(N, start=ord(start), stop=ord(stop))


def greekrange(N: int = 1):
    return urange(N, start='\u03b1')


def arabicrange(N: int = 1, **kwargs):
    start = kwargs.pop('start', 0)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [str(c) for c in range(start, stop)]


if __name__ == '__main__':

    lrange = latinrange(5, start='i')
    grange = greekrange(5)
    orange = ordrange(5)
    arange = arabicrange(5, start=1)

    abc = alphabet('latin', start='i')
    for i in range(6):
        print(next(abc))

    abc = alphabet('u')
    for i in range(6):
        print(next(abc))
