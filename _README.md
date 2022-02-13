# dewloosh.core

This package contains common developer utilities to support other `dewloosh` packages, such as

* Classes `DictCollection` and `OrderedDictCollection` providing facilities to deal with nested dictionaries, allowing us to create and manipulate hierarchical data objects. 

* A `Library` class, that takes `OrderedDictCollection` to the next level.

* A set of abstract base classes for metaprogramming.

* Various decorators, wrappers and other handy developer tools.

* Some other tools for educational refrencing.

Among all these, the most important one is the `Library` class, inherited by `dewloosh.geom.PolyData` or `dewloosh.solid.fem.FemMesh` for example. It is basically an ordered `defaultdict` with a self replicating default factory.

```python
>>> from dewloosh.core import Library
>>> obj = Library()
```

In every case where you'd want to use a dictionary, you can use a `Library` as a drop-in replacement, but on top of what a simple dictionary
provided, a `Library` is much more capable.

Let say we have a dictionary...