# -*- coding: utf-8 -*-
from dewloosh.core.types.library import Library
from typing import Callable
import numpy as np

__version__ = "0.0.dev9"
__description__ = "Common developer utilities and base classes to support other dewloosh packages."


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

