# **A Quick Guide**

## **Installation**
This is optional, but we suggest you to create a dedicated virtual enviroment at all times to avoid conflicts with your other projects. Create a folder, open a command shell in that folder and use the following command

```console
>>> python -m venv venv_name
```

Once the enviroment is created, activate it via typing

```console
>>> .\venv_name\Scripts\activate
```

`dewloosh.core` can be installed (either in a virtual enviroment or globally) from PyPI using `pip` on Python >= 3.6:

```console
>>> pip install dewloosh.core
```

## **Main Features**

### Wrapping

Wrapping may not be the most elegant solutions to inherit properties of a different class, but there are certain situations when it might save your life. One such a scenario is when you want to write an interface to a DeepDict that gets dinamically generated runtime, meaning, that the classes are simply not present at the time of writing your own code. This is when a wrapper comes handy. To wrap a dictionary, do the following:

```python
>>> from dewloosh.core import Wrapper
>>> data = {'a' : {'b' : {'c' : {'e' : 3}, 'd' : 2}}}
>>> wrapper = Wrapper(wrap=data)   
```

The `Wrapper` class channels down every call to the wrapped object (in this case a dictionary), if the object that the call is made upon is unable to answer the call by itself (because it misses the wanted attribute or method). The wrapped object is accessible through the `wrapped` property of the wrapper.

```python
>>> wrapper.wrapped
{'a': {'b': {'c': {'e': 3}, 'd': 2}}}
```

Note, that if for some reason we accidentally shadow a method in a base class like this:

```python
>>> class CustomWrapper(Wrapper):
>>>
>>>    def values(self, *args, **kwargs):
>>>        return None
```

Id we tried to wrap a dictionary now, the implementation would alter the bahaviour of the wrapper, leaving the behaviour of the wrapped object preserved and still accessible as ``CustomWrapper(wrap=data).wrapped.values()``.

```python
>>> CustomWrapper(wrap=data).wrapped.values()
dict_values([{'b': {'c': {'e': 3}, 'd': 2}}])
```

### Abstract Base Classes

The module `dewloosh.core.abc` provides simple classes to alleviate some of the unwanted consequences of the dynamically typed nature of Python. One of such a scenarios is when we subclass another class from a third-party library, because we want to inherit the functionality therein. But the stuff is complicated, and we probably woundn't want to go through all of it. Nevertheless, we want to make sure, that we don't brake the inner flow of the object at runtime, by overriding some essential methods, shadowing the original behaviour. Not like it wouldn't show up runtime sooner or later, but this leaves the door opened for bad code. Luckily, the problem can be solved fairly easily with some metaprogramming, and the meta submodule provides an abstract class `ABC_Safe` that can be used as a base class further down the line.

Running the following code throws an error at design time, because `foo` is already implemented in the parent class:

```python
>>> from dewloosh.core.abc import ABC_Safe
>>> 
>>> class Parent(ABC_Safe):
>>>     def foo(self):
>>>         pass
>>> 
>>> class Child(Parent):
>>>     def foo(self):
>>>         pass
```

Another important situation arises with abstract methods. Python provides a decorator for this out of the box, but again, not implemented abstract methods only show up at rumtime, which can easily be no time in the world of interpreted languages. The meta submodul is equipped with another abstract class called `ABC_Strong`, that makes you able to be informed about missing function implementations of a class right at design time. Here 'Strong' refers to the stronger requirement imposed on abstract methods. An abstract method in a child class is either implemented, or decorated with the `abstractmethod` decorator, which passes the ball to the next child. Obviously, you don't get to runtime, unless you implement all the required abstract classes. This is also useful if we want to create a template object, that provides instructions on how to complete a skeleton to have a working solution. A simple example to illustrate what happens if you brake the rules is the following:

```python
>>> from dewloosh.core.abc import ABC_Strong
>>> 
>>> class Parent(ABC_Strong):
>>>     @abstractmethod    
>>>     def foo(self):
>>>         pass
>>> 
>>> class Child(Parent):
>>>     ...
```

### Abstract Class Properties

Along the same thoughts, sometimes we want to ensure the existence of some class
properties when building complex objects with multiple base classes. This can be done using a special decorator:

```python
>>> from dewloosh.core.acp import abstract_class_property
>>> from abc import ABC
>>> 
>>> @abstract_class_property(prop1=int, prop2=float})
>>> class BaseClassA(ABC):
>>> 
>>>     prop1: int
>>>     prop2: list
>>> 
>>>     def __init__(self):
>>>         self.prop2 = [3, 4]
>>>         super().__init__()
>>>         return
```

### Infix Operators

Infix operators allow for a fancy way of defining binary operations using the operators '<<', '>>' and '|'.

```python
>>> from dewloosh.core.infix import Infix
>>> 
>>> mul = Infix(lambda x, y: x * y)
>>> 2 | mul | 4
8
>>> add = Infix(lambda x, y: x + y)
>>> 2 << add >> 4
6
```





