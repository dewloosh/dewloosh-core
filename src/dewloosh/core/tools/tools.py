# -*- coding: utf-8 -*-
import time
import sys
from collections.abc import Iterable
import six
from typing import Callable

__all__ = ['float_to_str_sig', 'floatformatter', 'issequence']


def floatformatter(*args, sig: int=6, **kwargs) -> str:
    """
    Returns a formatter, which essantially a string temapate
    ready to be formatted.
    
    Parameters
    ----------
    sig : int, Optional
        Number of significant digits. Default is 6.
        
    Returns
    -------
    string
        The string to be formatted.
    
    Examples
    --------    
    >>> from dewloosh.core import Library
    >>> data = Library()
    >>> data['a']['b']['c']['e'] = 1
    >>> data['a']['b']['d'] = 2
    >>> data.containers()
            
    """
    return "{" + "0:.{}g".format(sig) + "}"


def float_to_str_sig(value, *args, sig: int=6, atol: float=1e-7, 
                     **kwargs) -> str:
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
        Floating point tolerance. Values smaller than this 
        in the absolute sense are treated as zero.

    Returns
    -------
    string or a sequence of strings
        String representation of the provided input.
    
    Example
    --------
    Print the value of pi as a string with 4 significant digits:
    
    >>> from dewloosh.core.tools import float_to_str_sig
    >>> import math
    >>> float_to_str_sig(math.pi, sig=4)
    '3.142'
    
    """
    if not issequence(value):
        if atol is not None:
            if abs(value) < atol:
                value = 0.0
        return floatformatter(sig=sig).format(value)
    else:
        try:
            import numpy as np
        except ImportError:
            raise ImportError("You need numpy for this.")
        value = np.array(value)
        if atol is not None:
            inds = np.where(np.abs(value) < atol)[0]
            value[inds] = 0.0
        formatter = floatformatter(sig=sig)
        def f(v): return formatter.format(v)
        return list(map(f, value))


def timeit(fnc : Callable) -> float:
    """
    A simple decorator to measure execution time of a function.
    """
    def inner(*args, **kwargs):
        t0 = time.time()
        fnc(*args, **kwargs)
        t1 = time.time()
        return t1-t0
    return inner


def suppress(fnc: Callable) -> Callable:
    """
    Decorator that wraps a function to suppress it's calls to `print`.
    """
    def inner(*arg):
        original_stdout = sys.stdout
        sys.stdout = None
        res = fnc(*arg)
        sys.stdout = original_stdout
        return res
    return inner


def alphabet(abctype: str = 'latin', **kwargs) -> Iterable:
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


def ordrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 0)
    if isinstance(start, str):
        start = ord(start)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [chr(c) for c in range(start, stop)]


def latinrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 97)
    stop = kwargs.pop('stop', None)
    return ordrange(N, start=start, stop=stop)


def urange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', '\u0000')
    stop = kwargs.pop('stop', None)
    if stop is None:
        stop = start
    return ordrange(N, start=ord(start), stop=ord(stop))


def greekrange(N: int = 1) -> Iterable:
    return urange(N, start='\u03b1')


def arabicrange(N: int = 1, **kwargs) -> Iterable:
    start = kwargs.pop('start', 0)
    stop = kwargs.pop('stop', None)
    if stop is None or stop == start:
        stop = start + N
    return [str(c) for c in range(start, stop)]


def issequence(arg) -> bool:
    """
    Returns `True` if `arg` is any kind of iterable, but not a string,
    returns `False` otherwise.
    
    Examples
    --------
    The formatter to use to print a floating point number with 4 digits:
    
    >>> from dewloosh.core.tools import issequence
    >>> issequence([1, 2])
    True
    
    To print the actual value as a string:
    
    >>> issequence('lorem ipsum')
    False    
    """
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )  
