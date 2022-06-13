==============================================
Metaclasses - How to customize class behaviour
==============================================

In Python, everything is an object. Even a type of an object is an object, with a special type. These
classes are called metaclasses in Python. In normal situations you don't have to directly interact with
these classes, and the suggested way of inheritance is by using the abstract base classes in
`dewloosh.core.abc`. Likewise, if you want to customize the behaviour of a class, you can create your 
own metaclass by inheriting one of the classes of this module.

.. autoclass:: dewloosh.core.meta.ABCMeta_Weak
    :members: 

.. autoclass:: dewloosh.core.meta.ABCMeta_Strong
    :members: 

.. autoclass:: dewloosh.core.meta.ABCMeta_Safe
    :members: 