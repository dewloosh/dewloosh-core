# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 11:34:01 2019

Multiple solutions on how to enforce an abstract class property
on an object. Generic types like 'List[int]' are not allowed, 
because the don't work well with the isinstance()-like methods.

@author: Beni
"""
from abc import ABC

__all__ = ['abstract_class_property', 'setproperty']


def abstract_class_property(**kwargs):
    return abstract_class_property_B(**kwargs)


def setproperty(**kwargs):
    def decorator(cls):
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls
    return decorator


"""
Implementation A : class annotations solution using an object descriptor and a 
wrapper class with classic pythonic manipulations.
"""


def abstract_class_property_A(**kwargs):
    """
    Decorator function to decorate objects with abstract
    class properties. Leaves behind another decorator 
    that takes a class as its input.
    """

    def abstractor(WrappedClass):

        class PropertyWrapper(WrappedClass):
            """
            A Wrapper class to decorate objects with abstract class properties.
            The class has a default dummy annotation, just so that we can append 
            the items of the input dictionary d to the class definition.
            The dummy property is deleted at the end.
            """
            _dummy_: None

            def __init__(self, *args, **kwargs):
                WrappedClass.__init__(self)
                d_ = dict()
                d_props = PropertyWrapper.__dict__.get('__annotations__', {})
                for key, value in d_props.items():
                    d_[key] = value
                d_self = self.__class__.__dict__.get('__annotations__', {})
                for key, value in d_self.items():
                    d_[key] = value
                for key in d_.keys():
                    if not hasattr(self, key):
                        raise AttributeError(f'required attribute {key} not present '
                                             f'in {self.__class__}')
                return

        res = PropertyWrapper
        d_ = res.__dict__['__annotations__']
        for key, value in kwargs.items():
            d_[key] = value
        for key, value in WrappedClass.__dict__.get('__annotations__', {}).items():
            d_[key] = value
        del d_['_dummy_']
        return res

    return abstractor


"""
Implementation B : class annotations solution using an object descriptor and a 
wrapper class using the __mro__ property of the class.
This implementation also checks the validity of the declaration.
"""


def abstract_class_property_B(**kwargs):
    """
    Decorator function to decorate objects with abstract
    class properties. Leaves behind another decorator
    that takes a class as its input.
    """

    def abstractor(WrappedClass):

        class PropertyWrapper(WrappedClass):
            """
            A Wrapper class to decorate objects with abstract class properties.
            The class has a default dummy annotation, just so that we can append 
            the items of the input dictionary d to the class definition.
            The dummy property is deleted at the end.
            """
            _dummy_: None

            def __init__(self, *args, **kwargs):
                WrappedClass.__init__(self)
                self.__check_absclsprops__()
                return

            @classmethod
            def __absclsprops__(cls):
                """
                Collects the abstracts class properties and their
                expected types based on the MRO of the class.
                """
                t = cls.__mro__
                l = [ti.__dict__.get('__annotations__', {}) for ti in t]
                res = dict()
                for d in l:
                    for key, value in d.items():
                        res[key] = value
                return res

            def __check_absclsprops__(self):
                """
                Checks if the instance has attributes according to
                the anstract annotations. Returns True if every attribute is
                a type-correct declaration.
                """
                props = self.__class__.__absclsprops__()
                for key, value in props.items():
                    if not hasattr(self, key):
                        raise AttributeError(f'required attribute {key} not present '
                                             f'in {self.__class__}')
                    else:
                        if not isinstance(getattr(self, key), value):
                            raise TypeError(
                                'TypeError. key : {}, value = {}'.format(key, value))
                return True

        res = PropertyWrapper
        d_ = res.__dict__['__annotations__']
        for key, value in kwargs.items():
            d_[key] = value
        del d_['_dummy_']
        return res

    return abstractor


if __name__ == '__main__':

    @abstract_class_property_A(**{'customproperty1': int, 'customproperty2': float})
    class BaseClassA(ABC):

        prop1: int
        prop2: list

        def __init__(self):
            self.prop2 = [3, 4]
            super().__init__()
            return

    @setproperty(customproperty1=5)
    @abstract_class_property(customproperty3=bool)
    class ChildClassA(BaseClassA):

        prop1 = 5
        prop3: float

        def __init__(self):
            self.customproperty2 = 5.0
            self.customproperty3 = True
            self.prop3 = 1.0
            super().__init__()
            return

    @abstract_class_property_B(**{'customproperty1': int, 'customproperty2': float})
    class BaseClassB(ABC):

        prop1: int
        prop2: list

        def __init__(self):
            self.prop2 = [3, 4]
            super().__init__()
            return

    @setproperty(customproperty1=5)
    class ChildClassB(BaseClassB):

        prop1 = 5
        prop3: float

        def __init__(self):
            self.customproperty2 = 5.0
            self.prop3 = 1.0
            super().__init__()
            return

    """
    Commenting out the declaration prop1 generates
    an AttributeError. Note the difference of the 
    different implementations in the description of the error.
    """

    cA = ChildClassA()
    cB = ChildClassB()
    print('ChildClassA is instance of BaseClassA : {}'.format(
        isinstance(cA, BaseClassA)))
    print('ChildClassB is instance of BaseClassB : {}'.format(
        isinstance(cB, BaseClassB)))
    pass
