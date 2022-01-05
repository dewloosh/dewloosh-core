# -*- coding: utf-8 -*-
from dewloosh.core.types.defaultdict import OrderedDictCollection, \
    parsedicts
from dewloosh.core.tools.typing import issequence


class Library(OrderedDictCollection):

    def __init__(self, *args, parent=None, root=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self._root = root
        self._locked=False
    
    @property        
    def locked(self):
        return self._locked
    
    @locked.setter 
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value
    
    def lock(self):
        self._locked=True
        
    def unlock(self):
        self._locked=False

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
        dtype = Library if dtype is None else dtype
        return parsedicts(self, inclusive=inclusive, dtype=dtype, deep=deep)

    def __missing__(self, key):
        if self._locked:
            raise KeyError("Missing key : {}".format(key))
        else:
            return super().__missing__(key)

    def __join_parent__(self, parent: 'Library'):
        self.parent = parent
        self._root = parent.root()

    def __repr__(self):
        return dict.__repr__(self)

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
                if isinstance(value, Library):
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


if __name__ == '__main__':

    h = Library()
    h['a', 'b', 'c', 'e'] = 1
    #h['a']['b']['c']['e'] = 1
    h['a']['b']['d'] = 2

    b = h['a', 'b']
    b['e'] = 3
    b['f'] = 1, 2, 3
