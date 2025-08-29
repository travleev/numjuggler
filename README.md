# numjuggler
Tool to rename cells, surfaces, materials and universes in MCNP input files. See https://numjuggler.readthedocs.io


## Current status

[![Build Status](https://travis-ci.com/travleev/numjuggler.svg?branch=master)](https://travis-ci.com/travleev/numjuggler) -- shows status of the tests defined in [travis_tests](travis_tests) folder. 

[![PyPI version](https://badge.fury.io/py/numjuggler.svg)](https://badge.fury.io/py/numjuggler) -- available from PyPI. 

[![Documentation Status](https://readthedocs.org/projects/badge-demo/badge/?version=latest)](https://badge-demo.readthedocs.io/en/latest/?badge=latest) -- documentation


Information in the help message, returned by ``numjuggler -h mode`` is
outdated. Therefore, the best way to see all current modes is to search for
``args.mode == `` string in ``main.py``, and read comments in the correspondent
sections of code.

## Documentation

https://numjuggler.readthedocs.io should be considered as the main source of information. 

There is also a github repo [numjuggler.docs](https://github.com/inr-kit/numjuggler.docs) containing presentations and reports related to numjuggler. 

## Install
The numjuggler package is available at PyPI: https://pypi.org/project/numjuggler/. The preffered
way to install it using pip:

    >pip install numjuggler
    
Alternatively, one can clone from github and install in so-called development mode:

    >git clone git@github.com:travleev/numjuggler.git
    >cd numjuggler
    >pip install -e .

## Support the project

- Please report here any bugs or unclear behaviour,
- do not hesitate to propose new features to implement,
- Curerrent documentation is outdated and the code needs refactoring. Consider [sponsoring](https://github.com/sponsors/travleev) the project to support this activity.
- Travis CI is not more active for this repository. If you know alternatives or can help to organize CI for numjuggler -- let me know.


<!---

# numjuggler
Tool to rename cells, surfaces, materials and universes in MCNP input files. See https://numjuggler.readthedocs.io

## Install

You must have Python 2.7 installed on your machine (Python 3 was not tested but
might work). Unzip the  most recent archive from `dist` folder and run

    > python setup.py install --user

from the folder containing file `setup.py`. This installs the package, that can
be used from the command line in the following way:

    > python -m numjuggler ...

where ... -- are command line options specifying the input file and the rules
how cells, surfaces, etc. are renamed.

Alternatively, you can use [pip](https://pip.pypa.io/en/stable/) -- a tool for installing Python packages
(for some Python distributions it is included, otherwise must be installed separately). Unzipping the
archive in this case is not needed, and installation is done with the command

    > pip install numjuggler-X.X.X.tar.gz --user

When the package is installed with pip, a script called `numjuggler` is added to
`~/.local/bin` (or to `C:\Python27\Scripts`), so that invocation of the tool is
more simple. In this case, both two commands are identical:

    > numjuggler ...
    > python -m numjuggler ...

where .. -- are command line options.

## Help

After installing the package, run the following command to get some help and
instructions:

    > python -m numjuggler -h

There is also a github repo, [numjuggler.docs](https://github.com/inr-kit/numjuggler.docs), related to numjuggler documentation.

--->
