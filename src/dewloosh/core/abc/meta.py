# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


__all__ = ["ABCMeta_Weak", "ABCMeta_Strong", "ABCMeta_Safe", "ABC_Strong",
           "ABC_Weak", "ABC_Safe"]


class ABCMeta_Weak(ABCMeta):
    """
    Standard python metaclass. It follows weak abstraction in the meaning, that
    it is enough to implement the abstarcts in the instance, they impose no
    restriction on the inherited class itself. Therefore, error only occurs at
    runtime.
    """

    @staticmethod
    def _get_cls_methods(namespace, nomagic=False):
        """
        Returns the callable items in the namespace of the class.
        If `nomagic=False`, magic functions with trailing double 
        underscores are not returned.
        """
        if not nomagic:
            return {name for name, value in namespace.items()
                    if callable(value)}
        else:
            def cond(n, v): return callable(v) and ('__' not in n)
            return {name for name, value in namespace.items()
                    if cond(name, value)}


class ABC_Weak(metaclass=ABCMeta_Weak):
    """
    Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    __slots__ = ()


if __name__ == '__main__':

    """
    Explicit notation of an abstract method in a base class is
    not necessary. Error only occurs at runtime.
    """

    class ABC_Parent_Weak(ABC_Weak):

        @abstractmethod
        def abcParentWeak(self):
            pass

    class ABC_Child_Weak(ABC_Parent_Weak):

        @abstractmethod
        def abcChildWeak(self):
            pass

    class ABC_GrandChild_Weak(ABC_Child_Weak):

        @abstractmethod
        def abcGrandChildWeak(self):
            pass

    class GrandChild_Weak(ABC_GrandChild_Weak):
        """
        Comment out any of these implementations and witness how
        error arises on the line of object creation, but not during
        compilation.
        """

        def abcParentWeak(self):
            pass

        def abcChildWeak(self):
            pass

        def abcGrandChildWeak(self):
            pass

    grandchild_Weak = GrandChild_Weak()


class ABCMeta_Strong(ABCMeta_Weak):
    """
    Strong Python metaclass. It follows strong abstraction in the meaning, that
    an abstract function of any of the base classes must be implemented or
    delayed with the use of another @abstractmethod decorator.
    Error occurs at compilation time.
    """

    def __init__(self, name, bases, namespace, *args, **kwargs):
        super().__init__(name, bases, namespace, *args, **kwargs)

    def __new__(metaclass, name, bases, namespace, *args, **kwargs):
        cls = super().__new__(metaclass, name, bases, namespace, *args,
                              **kwargs)
        cls_methods = metaclass._get_cls_methods(namespace)
        for base in bases:
            base_abstracts = set()
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    base_abstracts.add(name)
            for abstract in base_abstracts:
                if abstract not in cls_methods:
                    err_str = """Can't create abstract class {classname}!
                    {classname} must implement abstract method {method} of
                    class {base_class}!""".format(
                        classname=name,
                        method=abstract,
                        base_class=base.__name__)
                    raise TypeError(err_str)
        return cls


class ABC_Strong(metaclass=ABCMeta_Strong):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    __slots__ = ()


class ABCMeta_Safe(ABCMeta_Weak):
    """
    Python metaclass for safe inheritance. Throws a TypeError
    if a method tries to shadow a definition in any of the base
    classes.
    """

    def __init__(self, name, bases, namespace, *args, **kwargs):
        super().__init__(name, bases, namespace, *args, **kwargs)

    def __new__(metaclass, name, bases, namespace, *args, **kwargs):
        cls = super().__new__(metaclass, name, bases, namespace, *args,
                              **kwargs)
        cls_methods = metaclass._get_cls_methods(namespace, nomagic=True)
        for base in bases:
            for method in cls_methods:
                if hasattr(base, method):
                    err_str = """Can't create abstract class {classname}!
                        Method {method} is already implemented in class
                        {base_class}!""".format(
                        classname=name,
                        method=method,
                        base_class=base.__name__)
                    raise TypeError(err_str)
        return cls


class ABC_Safe(metaclass=ABCMeta_Safe):
    """
    Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    __slots__ = ()


if __name__ == '__main__':

    """
    The code below throws a TypeError if an abstract method is not
    included in the definition of child class.
    Error occurs at compilation time.
    """

    class ABC_Parent_Strong(ABC_Strong):

        @abstractmethod
        def abcParentStrong(self):
            pass

    class ABC_Child_Strong(ABC_Parent_Strong):

        @abstractmethod
        def abcParentStrong(self):
            pass

        @abstractmethod
        def abcChildStrong(self):
            pass

    class ABC_GrandChild_Strong(ABC_Child_Strong):

        @abstractmethod
        def abcParentStrong(self):
            pass

        @abstractmethod
        def abcChildStrong(self):
            pass

        @abstractmethod
        def abcGrandChildStrong(self):
            pass

    class GrandChild_Strong(ABC_GrandChild_Strong):

        def abcParentStrong(self):
            pass

        def abcChildStrong(self):
            pass

        def abcGrandChildStrong(self):
            pass

    grandchild_Strong = GrandChild_Strong()

    class ABC_Parent_Safe(ABC_Safe):

        def funcParentSafe(self):
            pass

    class ABC_Child_Safe(ABC_Parent_Safe):

        def funcChildSafe(self):
            pass

    class ABC_GrandChild_Safe(ABC_Child_Safe):

        def _funcParentSafe(self):
            pass
