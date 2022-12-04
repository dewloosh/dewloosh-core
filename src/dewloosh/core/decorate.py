# -*- coding: utf-8 -*-
from typing import Callable
import numpy as np
from numpy import ndarray


__all__ = ['squeeze']


def squeeze_if_array(arr):
    return np.squeeze(arr) if isinstance(arr, ndarray) else arr


def squeeze(default=True):
    def decorator(fnc: Callable):
        def inner(*args, squeeze:bool=default, **kwargs):
            if squeeze:
                res = fnc(*args, **kwargs)
                if isinstance(res, tuple):
                    return list(map(squeeze_if_array, res))
                elif isinstance(res, dict):
                    return {k : squeeze_if_array(v) for k, v in res.items()}
                else:
                    return squeeze_if_array(res)
            else:
                return fnc(*args, **kwargs)
        inner.__doc__ = fnc.__doc__
        return inner
    return decorator