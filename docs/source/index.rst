.. dewloosh.core documentation master file, created by
   sphinx-quickstart on Wed Jun  1 20:23:30 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dewloosh.core
=============

.. warning::
    This package is under active development and in an alpha stage. Come back later,
    or star the GitHub repo to make sure you don't miss the first stable release!

The main purpose of `dewloosh.core` is to provide batteries to other dewloosh
projects, and to provide a set of common developer tools for the public.

Features
--------

* | Various dictionary classes that enhance the core behaviour of the built-in
  | `dict` type. The top of the cake is the `Library` class, which offers a different
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



