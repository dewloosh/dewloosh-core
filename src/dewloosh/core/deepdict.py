# -*- coding: utf-8 -*-
# http://stackoverflow.com/a/6190500/562769
from typing import Hashable, Union
from collections.abc import Iterable
import six

from .tools.dtk import dictparser, parseitems, parseaddress, parsedicts


__all__ = ['DeepDict']


NoneType = type(None)


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


class DeepDict(dict):
    """
    An nested dictionary class with a self-replicating default factory. 
    It can be a drop-in replacement for the bulit-in dictionary type, 
    but it's more capable as it handles nested layouts.
    
    Examples
    --------
    Basic usage:
    
    >>> from nddict import DeepDict
    >>> d = {'a' : {'aa' : {'aaa' : 0}}, 'b' : 1, 'c' : {'cc' : 2}}
    >>> dd = DeepDict(d)
    >>> list(dd.values(deep=True))
    [0, 1, 2]
    
    See the docs for more use cases!
        
    """
    
    def __init__(self, *args, parent=None, root=None, locked=None, **kwargs):
        """
        Returns a `DeepDict` instance.

        Parameters
        ----------
        *args : tuple, Optional
            Extra positional arguments are forwarded to the `dict` class.

        parent : `DeepDict`, Optional
            Parent `DeepDict` instance. Default is `None`.

        root : `DeepDict`, Optional
            The top-level object. It is automatically set when creating nested
            layouts, but may be explicitly provided. Default is `None`. 

        locked : bool or NoneType, Optional
            If the object is locked, it reacts to missing keys as a regular dictionary would.
            If it is not, a new level and a new child is created (see the examples in the docs).
            A `None` value means that in terms of locking, the state of the object 
            is inherited from its parent. Default is `None`.

        **kwargs : tuple, Optional
            Extra keyword arguments are forwarded to the `dict` class.

        """
        super().__init__(*args, **kwargs)
        self.parent = parent
        self._root = root
        self._locked = locked
        self._key = None
        
    @property
    def key(self) -> Union[Hashable, NoneType]:
        """
        Returns the key of the dictionary in its parent, or `None` if the 
        object is the root.
        """
        return self._key
           
    @property
    def locked(self) -> bool:
        """
        Returns `True` if the object is locked. The property is equpped with a setter.
        """
        if self.parent is None:
            return self._locked if isinstance(self._locked, bool) else False
        else:
            return self._locked if isinstance(self._locked, bool) else self.parent.locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    @property
    def depth(self) -> int:
        """
        Retuns the depth of the actual instance in a layout, starting from 0..
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1

    def lock(self):
        """
        Locks the layout of the dictionary. If a `DeepDict` is locked,
        missing keys are handled the same way as they would've been handled
        if it was a ´dict´.        

        Equivalent to ``self.locked = True``.
        """
        self._locked = True

    def unlock(self):
        """
        Releases the layout of the dictionary. If a `DeepDict` is not locked,
        a missing key creates a new level in the layout.

        Equivalent to ``self.locked = False``.
        """
        self._locked = False

    def root(self):
        """
        Returns the top-level object in a nested layout.
        """
        if self.parent is None:
            return self
        else:
            if self._root is not None:
                return self._root
            else:
                return self.parent.root()

    def is_root(self) -> bool:
        """
        Returns `True`, if the object is the root.
        """
        return self.parent is None

    def containers(self, *args, inclusive=False, deep=True, dtype=None, **kwargs):
        """
        Returns all the containers in a nested layout. A dictionary in a nested layout
        is called a container, only if it contains other containers (it is a parent). 

        Parameters
        ----------
        inclusive : bool, Optional
            If `True`, the object the call is made upon also gets returned.
            This can be important if you make the call on the root object, which most
            of the time does not hold onto relevant data directly.
            Default is `False`.

        deep : bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`

        dtype : Any, Optional
            Constrains the type of the returned objects.
            Default is `None`, which means no restriction.

        Returns
        -------
        generator
            Returns a generator object.

        Examples
        --------
        A simple example:

        >>> from nddict import DeepDict
        >>> data = DeepDict()
        >>> data['a', 'b', 'c'] = 1
        >>> [c.key for c in data.containers()]
        ['a', 'b']

        We can see, that dictionaries 'a' and 'b' are returned as containers, but 'c' 
        isn't,  because it is not a parent, there are no deeper levels. 

        >>> [c.key for c in data.containers(inclusive=True, deep=True)]
        [None, 'a', 'b']

        >>> [c.key for c in data.containers(inclusive=True, deep=False)]     
        [None, 'a']

        >>> [c.key for c in data.containers(inclusive=False, deep=True)]       
        ['a', 'b']

        >>> [c.key for c in data.containers(inclusive=False, deep=False)]      
        ['a']

        """
        dtype = self.__class__ if dtype is None else dtype
        return parsedicts(self, inclusive=inclusive, dtype=dtype, deep=deep)

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
                if isinstance(value, DeepDict):
                    value.__join_parent__(self, key)
                return super().__setitem__(key, value)
        except AttributeError:
            raise RuntimeError(
                "Target is of type '{}', which is not a container.".format(type(d)))
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.locked:
            raise KeyError("Missing key : {}".format(key))
        if issequence(key):
            if key[0] not in self:
                self[key[0]] = value = self.__class__()
            else:
                value = self[key[0]]
            if len(key) > 1:
                return value.__missing__(key[1:])
            else:
                return value
        else:
            self[key] = value = self.__class__()
            return value
        
    def __reduce__(self):
        return self.__class__, tuple(), None, None, self.items()
    
    def __repr__(self):
        frmtstr = self.__class__.__name__ + '(%s)'
        return frmtstr % (dict.__repr__(self))
       
    def __join_parent__(self, parent, key: Hashable = None):
        self.parent = parent
        self._root = parent.root()
        self._key = key

    def items(self, *args, deep=False, return_address=False, **kwargs):
        if deep:
            if return_address:
                for addr, v in dictparser(self):
                    yield addr, v
            else:
                for k, v in parseitems(self):
                    yield k, v
        else:
            for k, v in super().items():
                yield k, v

    def values(self, *args, deep=False, return_address=False, **kwargs):
        if deep:
            if return_address:
                for addr, v in dictparser(self):
                    yield addr, v
            else:
                for _, v in parseitems(self):
                    yield v
        else:
            for v in super().values():
                yield v

    def keys(self, *args, deep=False, return_address=False, **kwargs):
        if deep:
            if return_address:
                for addr, _ in dictparser(self):
                    yield addr
            else:
                for k, _ in parseitems(self):
                    yield k
        else:
            for k in super().keys():
                yield k
