# ZFBrain

[![Documentation Status](https://readthedocs.org/projects/zfbrain/badge/?version=latest)](https://zfbrain.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.com/hneustadter/ZFBrain.svg?branch=master)](https://travis-ci.com/hneustadter/ZFBrain)


## Usage
ZFBrain displays an interactive visualization of the Zebra Finch brain in 3D. The software presents the brain regions important for vocalization, including the HVC, RA, and Area X. It is intended to be used as an aid for researchers studying these brain regions.

## Installations
ZFBrain can be installed through the "Releases" tab on the right, where you should download the release version that is compatible with your operating system. This software was developed for use on Windows, MacOS, and Linux.

## Screenshots
ZFBrain application in Windows:
![image](https://user-images.githubusercontent.com/72104561/111705780-9f1c7600-8817-11eb-8623-646abe2ed996.png)

## Development

Make sure you are in the top-level directory ("ZFBrain"). 

To run the main program, type (`$` refers to command line prompt)

`$ python zfbrain`

To run all unit tests, type

`$ python -m unittest -v`

(the `-v` option stands for "verbose" and lists each test that is run)

## Contributing

Contributions to ZFBrain are welcome!

The preferred method of submitting a change is by making a pull request on GitHub against the "master" branch.

The documentation is generated using Sphinx.
