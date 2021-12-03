# -*- coding: utf-8 -*-
from collections import Iterable
import six


def issequence(arg):
    """
    A sequence is an iterable, but not any kind of string.
    """
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )
