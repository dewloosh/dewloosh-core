================================================================
DewLoosh.Core - Common Developer Utilities for DewLoosh Projects
================================================================

`DewLoosh` is a rapid prototyping platform focused on numerical calculations 
mainly corcerned with simulations of natural phenomena. It provides a set of common 
functionalities and interfaces with a number of state-of-the-art open source 
packages to combine their power seamlessly under a single developing 
environment.

The main purpose of `dewloosh.core` is to provide batteries to other dewloosh
projects.

Features
--------

* | Various dictionary classes that enhance the core behaviour of the built-in
  | `dict` type. The top of the cake is the `DeepDict` class, which offers a different
  | behaviour for nested dictionaries by applying a self replicating defalt factory.

* | A set of tools for metaprogramming. The use cases include declaring custom abstract 
  | class properties, using metaclasses to avoid unwanted code conflicts, assuring the 
  | implementation of abstract methods at design time, etc.

* Decorators, wrappers and other handy developer tools.

Check out the :doc:`user_guide` section for further information.

Contents
--------

.. toctree::
   :maxdepth: 3
   
   user_guide
   api
   
Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



