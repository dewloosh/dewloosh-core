# -*- coding: utf-8 -*-
from dewloosh.core.types.defaultdict import OrderedDictCollection


class Hierarchy(OrderedDictCollection):

    def __init__(self, *args, parent=None, root=None, **kwargs):
        super().__init__()
        self.parent = parent
        self._root = root

    def root(self):
        if self.parent is None:
            return self
        else:
            if self._root is not None:
                return self._root
            else:
                return self.parent.root()

    def is_root(self):
        return self.parent is None

    def containers(self, *args, inclusive=False, deep=True, dtype=None, **kwargs):
        dtype = Hierarchy if dtype is None else dtype
        return parsedicts(self, inclusive=inclusive, dtype=dtype, deep=deep)

    def __join_parent__(self, parent: 'Hierarchy'):
        self.parent = parent
        self._root = parent.root()

    def __repr__(self):
        return 'Hierarchy(%s)' % (dict.__repr__(self))

    def __setitem__(self, key, value):
        try:
            if isinstance(key, tuple):
                if not key[0] in self:
                    d = self.__missing__(key[0])
                else:
                    d = self[key[0]]
                if len(key) > 1:
                    d.__setitem__(key[1:], value)
                else:
                    self[key[0]] = value
            else:
                if isinstance(value, Hierarchy):
                    value.__join_parent__(self)
                return super().__setitem__(key, value)
        except AttributeError:
            raise RuntimeError("Target is of type '{}', which is not \
                               a container.".format(type(d)))
        except KeyError:
            return self.__missing__(key)

    def default_factory(self):
        cls = type(self)
        return cls(parent=self, root=self.root())


def parsedicts(d: dict = None, *args, inclusive=True, dtype=dict,
               deep=True, **kwargs):
    if inclusive:
        if isinstance(d, dtype):
            yield d
    for value in d.values():
        if isinstance(value, dtype):
            yield value
            if deep:
                for subvalue in parsedicts(value, inclusive=False,
                                           dtype=dtype):
                    yield subvalue


if __name__ == '__main__':

    h = Hierarchy()
    h['a']['b']['c']['e'] = 1
    h['a']['b']['d'] = 2

    b = h['a', 'b']
    b['e'] = 3
    b['f'] = 1, 2, 3
