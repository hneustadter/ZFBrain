.. _developer-guide:

Developer\'s Guide
******************

.. toctree::
    :hidden:

Contributions to ZFBrain are welcome! 
This section gives function and class definitions used in the development of ZFBrain. 

Future Development
---------

We are currently working on implementing the following changes to ZFBrain:

* Add more brain regions

* Make all current and future brain regions more anatomically correct

* Improve the shading and colors of the brain regions

* Make the executable easier to install

* Add a plane to see a 2D slice of the brain

Docstrings
----------

ZFBrain uses a style derived from NumPy's docstrings style, which includes giving
the types of function arguments. The functions used to generate the ZFBrain surface can be seen in our `API section <https://zfbrain.readthedocs.io/en/latest/zfbrain.html>`_.

Contributions
-------------

Follow these steps if you are interested in contributing to ZFBrain:

* Go to our `GitHub <https://github.com/hneustadter/ZFBrain>`_ page and make your own copy of ZFBrain by clicking on the "fork" button in the top right corner.

* Clone the project to your computer using a text editor. We recommend using the Visual Studio Code text editor, which is what we used to originally make ZFBrain. You can download a copy of the ZFBrain code on our GitHub page by pressing the green "Code" button. This will open a drop down window in which you can copy the URL by clicking on the clipboard figure. In the terminal of your text editor, type `git clone` and then paste the URL you copied from GitHub.

* Make sure you are working in the correct directory by typing `cd zfbrain` in the terminal of the text editor.

Documentation
-------------

Documentation is generated with sphinx and hosted on ReadTheDocs. To generate documentation
locally, make sure you are in the "docs" subfolder and type `cmd make.bat` in the terminal. 
Then run `start make.bat` in the terminal, which will open up another window. 
In this new terminal, type `make html`. Then, the documentation can be found locally in the "docs/html" folder. 
The "homepage" is the `index.rst` file.

Testing
-------

ZFBrain uses the python unittest package for testing and Travis runs these tests on every
commit. To run tests locally before submitting a PR, make sure you are in the home directory
of ZFBrain and type `python3 -m unittest -v`.