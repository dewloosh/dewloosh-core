# -*- coding: utf-8 -*-
from typing import Callable
import numpy as np


def squeeze(default=True):
    def decorator(fnc: Callable):
        def inner(*args, **kwargs):
            if kwargs.get('squeeze', default):
                res = fnc(*args, **kwargs)
                if isinstance(res, tuple):
                    return list(map(np.squeeze, res))
                return np.squeeze(res)
            else:
                return fnc(*args, **kwargs)
        return inner
    return decorator