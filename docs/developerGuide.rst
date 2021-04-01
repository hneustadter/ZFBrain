.. _developer-guide:

Developer\'s Guide
******************

.. toctree::
    :hidden:

This section gives function and class definitions used in the development of 
ZFBrain. 

Todo list
---------

Here is a list of things that we would like to implement in the future:

* item 1

* item 2

Docstrings
----------

ZFBrain uses a style derived from NumPy's docstrings style, which includes giving
the types of function arguments.

Documentation
-------------

Documentation is generated with sphinx and hosted on ReadTheDocs. To generate documentation
locally, make sure you are in the "docs" subfolder and type `make html` in a terminal. Then,
the documentation can be found locally in the "docs/html" folder. The "homepage" is the 
`index.rst` file.

Testing
-------

ZFBrain uses the python unittest package for testing and Travis runs these tests on every
commit. To run tests locally before submitting a PR, make sure you are in the home directory
of ZFBrain and type `python3 -m unittest -v`.