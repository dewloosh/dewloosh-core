# **dewloosh.core**

<a href='https://dewloosh-core.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/dewloosh-core/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://pypi.org/project/dewloosh.core"/>
            <img src="https://badge.fury.io/py/dewloosh.core.svg"/>
</a>
<a href="https://opensource.org/licenses/MIT"/>
            <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/>
</a>


This package contains common developer utilities to support other `dewloosh` solutions. Everything is pure Python, the package requires no extra dependencies and should run on a minimal setup.

The most important features:

* Various dictionary classes that enhance the core behaviour of the built-in `dict` type. The top of the cake is the `DeepDict` class, which offers a different behaviour for nested dictionaries by applying a self replicating defalt factory.

* A set of tools for metaprogramming. The use cases include declaring custom abstract class properties, using metaclasses to avoid unwanted code conflicts, assuring the implementation of abstract methods at design time, etc.

* Decorators, wrappers and other handy developer tools.

## **Documentation and Issues**

Click [here](https://dewloosh-core.readthedocs.io/en/latest/) to read the documentation.

There are no known issues.

## **A Quick Guide**

#### Dictionaries of dictionaries of diactionaries of ...

In every case where you'd want to use a `dict`, you can use a `Deepdict` as a drop-in replacement, but on top of what a simple dictionary provides, a `Deepdict` is more capable, as it provides a machinery to handle nested layouts. It is basically an ordered `defaultdict` with a self replicating default factory. 

```python
>>> from dewloosh.core import Deepdict
>>> data = Deepdict()
```

A `Deepdict` is essentially a nested default dictionary. Being nested refers to the fact that you can do this:

```python
>>> data['a']['b']['c']['e'] = 1
>>> data['a']['b']['d'] = 2
```

Notice that the object carves a way up until the last key, without needing to create each level explicitly. What happens is that every time a key is missing in a `data`, the object creates a new instance, which then is also ready to handle missing keys or data. Accessing nested subdictionaries works in a similar fashion:

```python
>>> data['a']['b']['c']['e']
1
```
To allow for a more Pythonic feel, it also supports array-like indexing, so that the following operations are valid: 

```python
>>> data['a', 'b', 'c', 'e'] = 3
>>> data['a', 'b', 'c', 'e']
3
```

Of course, this is something that we can easily replicate using pure Python in one line, without the need for fancy stuff:

```python
>>> data = {'a' : {'b' : {'c' : {'e' : 3}, 'd' : 2}}}    
```

The key point is that we loop over a pure `dict` instance, we get

```python
>>> [k for k in data.keys()]
['a']    
```

But if we use a `Deepdict` class and the option `deep=True` when accessing
keys, values or items of dictionaries, the following happens: 

```python
>>> [k for k in Deepdict(data).keys(deep=True)]
['e', 'd']    
```

We can see, that in this case, iteration goes over keys, that actually hold on to some data, and does not return the containers themselves. If we do the same experiment with the values, it shows that the `Deepdict` only returns the leafs of the data-tree and the behaviour is fundamentally different:

```python
>>> [k for k in data.values()]
[{'b': {'c': {'e': 3}, 'd': 2}}]    
```

```python
>>> [k for k in Deepdict(data).values(deep=True)]
[3, 2]    
```

It is important, that the call `obj.values(deep=True)` still returns a generator object, which makes it memory efficient when looping over large datasets.

```python
>>> Deepdict(data).values(deep=True)
<generator object OrderedDefaultDict.values at 0x0000028F209D54A0>    
```

#### Wrapping

Wrapping may not be the most elegant solutions to inherit properties of a different class, but there are certain situations when it might save your life. One such a scenario is when you want to write an interface to a Deepdict that gets dinamically generated runtime, meaning, that the classes are simply not present at the time of writing your own code. This is when a wrapper comes handy. To wrap a dictionary, do the following:

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

#### Abstract Classes and Metaprogramming

The submodule `dewloosh.core.abc` provides simple classes to alleviate some of the unwanted consequences of the dynamically typed nature of Python. One of such a scenarios is when we subclass another class from a third-party Deepdict, because we want to inherit the functionality therein. But the stuff is complicated, and we probably woundn't want to go through all of it. Nevertheless, we want to make sure, that we don't brake the inner flow of the object at runtime, by overriding some essential methods, shadowing the original behaviour. Not like it wouldn't show up runtime sooner or later, but this leaves the door opened for bad code. Luckily, the problem can be solved fairly easily with some metaprogramming, and the meta submodule provides an abstract class `ABC_Safe` that can be used as a base class further down the line.

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

#### Abstract Class Properties

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

#### Infix Operators

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

## **Testing**

To run all tests, open up a console in the root directory of the project and type the following

```console
>>> python -m unittest
```

## **Dependencies**

The package has no dependencies.

## **License**

This package is licensed under the MIT license.