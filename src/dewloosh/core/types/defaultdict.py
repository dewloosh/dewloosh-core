# -*- coding: utf-8 -*-
from typing import Union, Callable
from collections import OrderedDict
from copy import deepcopy, copy

from ..tools import issequence


__all__ = ["DefaultDict", "OrderedDefaultDict", "NestedDict",
           "NestedOrderedDict", "dictparser"]


class DefaultDict(dict):
    """
    Implements a defaultdict.
    Source: http://stackoverflow.com/a/6190500/562769
    """

    def __init__(self, default_factory: Callable = None, *args, **kwargs):
        if (default_factory is not None and
                not hasattr(default_factory, '__call__')):
            raise TypeError('first argument must be callable')
        super().__init__(*args, **kwargs)
        if default_factory is not None:
            self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        return type(self)(self.default_factory,
                          deepcopy(self.items()))

    def __repr__(self):
        return 'defaultdict(%s, %s)' % (self.default_factory,
                                        dict.__repr__(self))

    def items(self, *args, deep=False, return_address=False, **kwargs):
        if deep:
            if return_address:
                return dictparser(self)
            else:
                return parseitems(self)
        else:
            for k, v in super().items():
                yield k, v

    def values(self, *args, deep=False, **kwargs):
        if deep:
            for _, v in parseitems(self):
                yield v
        else:
            for v in super().values():
                yield v

    def keys(self, *args, deep=False, **kwargs):
        if deep:
            for k, _ in parseitems(self):
                yield k
        else:
            for k in super().keys():
                yield k

    @classmethod
    def default_factory(cls):
        return cls()


class OrderedDefaultDict(OrderedDict):
    """
    Implements an ordered version of a defaultdict.
    Source: http://stackoverflow.com/a/6190500/562769
    """

    def __init__(self, default_factory: Callable = None, *args, **kwargs):
        if (default_factory is not None and
                not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        super().__init__(*args, **kwargs)
        if default_factory is not None:
            self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        return type(self)(self.default_factory,
                          deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               dict.__repr__(self))

    def items(self, *args, deep=False, return_address=False, **kwargs):
        if deep:
            if return_address:
                for k, v in dictparser(self):
                    yield k, v
            else:
                for k, v in parseitems(self):
                    yield k, v
        else:
            for k, v in super().items():
                yield k, v

    def values(self, *args, deep=False, **kwargs):
        if deep:
            for _, v in parseitems(self):
                yield v
        else:
            for v in super().values():
                yield v

    def keys(self, *args, deep=False, **kwargs):
        if deep:
            for k, _ in parseitems(self):
                yield k
        else:
            for k in super().keys():
                yield k

    @classmethod
    def default_factory(cls):
        return cls()


class DictCollection(DefaultDict):

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

    def __repr__(self):
        return 'DictCollection(%s)' % dict.__repr__(self)

    def __getitem__(self, key):
        try:
            if issequence(key):
                return parseaddress(self, key)
            else:
                return super().__getitem__(key)
        except ValueError:
            return self.__missing__(key)
        except KeyError:
            return self.__missing__(key)

    def __setitem__(self, key, value):
        try:
            if issequence(key):
                if not key[0] in self:
                    d = self.__missing__(key[0])
                else:
                    d = self[key[0]]
                if len(key) > 1:
                    d.__setitem__(key[1:], value)
                else:
                    self[key[0]] = value
            else:
                return super().__setitem__(key, value)
        except AttributeError:
            raise RuntimeError(
                "Target is of type '{}', which is not a container.".format(type(d)))
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if issequence(key):
            if key[0] not in self:
                self[key[0]] = value = self.default_factory()
            else:
                value = self[key[0]]
            if len(key) > 1:
                return value.__missing__(key[1:])
            else:
                return value
        else:
            self[key] = value = self.default_factory()
            return value


class OrderedDictCollection(OrderedDefaultDict):

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

    def __repr__(self):
        return 'OrderedDictCollection(%s)' % dict.__repr__(self)

    def __getitem__(self, key):
        try:
            if issequence(key):
                return parseaddress(self, key)
            else:
                return super().__getitem__(key)
        except ValueError:
            return self.__missing__(key)
        except KeyError:
            return self.__missing__(key)

    def __setitem__(self, key, value):
        try:
            if issequence(key):
                if not key[0] in self:
                    d = self.__missing__(key[0])
                else:
                    d = self[key[0]]
                if len(key) > 1:
                    d.__setitem__(key[1:], value)
                else:
                    self[key[0]] = value
            else:
                return super().__setitem__(key, value)
        except AttributeError:
            raise RuntimeError(
                "Target is of type '{}', which is not a container.".format(type(d)))
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if issequence(key):
            if key[0] not in self:
                self[key[0]] = value = self.default_factory()
            else:
                value = self[key[0]]
            if len(key) > 1:
                return value.__missing__(key[1:])
            else:
                return value
        else:
            self[key] = value = self.default_factory()
            return value


def NestedDict(ordered: bool = False) -> Union[DefaultDict,
                                               OrderedDefaultDict]:
    """
    Returns a nested default dictionary.
    """
    if ordered:
        return OrderedDefaultDict(lambda *_: NestedDict(ordered))
    else:
        return DefaultDict(lambda *_: NestedDict(ordered))


def NestedOrderedDict() -> OrderedDefaultDict:
    """
    Returns a nested and ordered default dictionary.
    """
    return OrderedDefaultDict(lambda *_: NestedOrderedDict())


def parseaddress(d: dict, a: list):
    if not isinstance(d, dict):
        raise ValueError
    if not a[0] in d:
        raise KeyError(a[0])
    if len(a) > 1:
        return parseaddress(d[a[0]], a[1:])
    else:
        return d[a[0]]


def parseitems(d: dict = None, *args, dtype=dict, **kwargs):
    """
    A generator function that yields all the items of a nested dictionary as
    (key, value) pairs.

    Notes
    -----
        Does not return nested dictionaries themselves, only their content.
    """
    for key, value in d.items():
        if isinstance(value, dtype):
            for data in parseitems(value, dtype=dtype):
                yield data
        else:
            yield key, value


def dictparser(d: dict = None, address=[], *args, dtype=dict, **kwargs):
    """
    Iterates through all the values of a nested dictionary.

    Notes
    -----
        Returns all kinds of items, even nested discionaries themselves,
        along with their content.
    """
    for key, value in d.items():
        subaddress = copy(address)
        subaddress.append(key)
        if isinstance(value, dtype):
            for data in dictparser(value, subaddress, dtype=dtype):
                yield data
        else:
            yield subaddress, value


def parsedicts_addr(d: dict = None, address=[], *args, inclusive=True,
                    dtype=dict, deep=True, **kwargs):
    if inclusive:
        if isinstance(d, dtype):
            yield address, d
    for key, value in d.items():
        if isinstance(value, dtype):
            addr = copy(address)
            addr.append(key)
            yield addr, value
            if deep:
                for subaddr, subval in \
                    parsedicts_addr(value, addr,
                                    inclusive=False, dtype=dtype):
                    yield subaddr, subval


def parsedicts(d: dict = None, *args, inclusive=True, dtype=dict,
               deep=True, **kwargs):
    if inclusive:
        if isinstance(d, dtype):
            yield d
    for value in d.values():
        if isinstance(value, dtype):
            yield value
            if deep:
                for subvalue in \
                        parsedicts(value, inclusive=False, dtype=dtype):
                    yield subvalue


if __name__ == '__main__':

    factory = lambda *_: 'none'

    dd = DefaultDict(factory)
    print(dd['key'])

    ndd = NestedDict(ordered=False)
    ndd['a']['b']['c']['e'] = 1
    ndd['a']['b']['d'] = 2
    print(ndd['a']['b']['c'])
    print(ndd['a']['b']['d'])

    for k, v in ndd.items():
        print((k, v))

    for v in ndd.values():
        print(v)

    for k in ndd.keys():
        print(k)

    for k in ndd.keys(deep=True):
        print(k)

    for k, v in ndd.items(deep=True):
        print((k, v))

    for a, v in ndd.items(deep=True, return_address=True):
        print((a, v))

    def foo(*a):
        print(type(a))

    dc = OrderedDictCollection()
    dc['a']['b']['c']['e'] = 1
    dc['a']['b']['d'] = 2

    for v in dc.values():
        print(v)

    for k in dc.keys():
        print(k)

    for k in dc.keys(deep=True):
        print(k)
