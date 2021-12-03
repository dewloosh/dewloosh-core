from collections import OrderedDict
from copy import copy


class NestedOrderedDict(OrderedDict):
    """
    A nested dictionary hierarchy.
    """

    separator = '::'

    def __init__(self, *args, parent=None, separator=None, key=None,
                 name=None, dtype=None, ftype=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        if parent is not None:
            assert isinstance(parent, dict)
            self.parent = parent
            self.separator = self.parent.separator
        if separator is not None:
            self.separator = separator
        self._key = key
        self._name = name
        self.dtype = dtype if dtype is not None else type(self)
        self.ftype = ftype if ftype is not None else type(self)
        self._key_to_address_mapper = None

    def parser(self, address=None, *args, **kwargs):
        """
        Iterates through the values of a dictionary.

        Usage
        -----
            (1) If the keyword 'inclusive' is provided as True, returns root
                as the first item.
            (2) If 'relative' is in args, addresses are measured relative to
                the calling Hierarchy.
        Notes
        -----
            (1) Returns all kinds of items.
        """
        if address is None:
            address = [] if 'relative' in args else self.address

        if kwargs.pop('inclusive', False):
            yield address, self.key, self

        for key, value in self.items():
            if isinstance(value, self.ftype):
                subaddress = copy(address)
                subaddress.append(key)
                yield subaddress, key, value
            elif isinstance(value, self.dtype):
                subaddress = copy(address)
                subaddress.append(key)
                for parsedata in value.parser(subaddress):
                    yield parsedata


def dictparser(d: dict = None, address=None, *args, **kwargs):
    """
    Iterates through all the values of a nested dictionary.

    Notes
    -----
        (1) Returns all kinds of items.
    """
    if address is None:
        address = []
    for key, value in d.items():
        subaddress = copy(address)
        subaddress.append(key)
        yield subaddress, key, value
        if isinstance(value, dict):
            for data in dictparser(value, subaddress):
                yield data


if __name__ == '__main__':

    d = NestedOrderedDict({0: 1, 1: 2})
    e = NestedOrderedDict({2: 3, 3: 4})
    f = NestedOrderedDict({22: 13, 23: 54})
    g = NestedOrderedDict({24: 8, 73: 11})
    e['f'] = f
    e['g'] = g
    d['e'] = e

    print(list(d.values()))

    def foo(d):
        def yielder(x):
            yield x
        #isdict = lambda v : isinstance(v, dict)
        def isnotdict(v): return not isinstance(v, dict)
        vals = d.values()
        nodicts = list(filter(isnotdict, vals))
        while True:
            [yielder(v) for v in nodicts]
            #dicts = list(filter(isdict, vals))
