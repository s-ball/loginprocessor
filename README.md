# loginprocessor

## Description

This module provides a BaseHandler implementation that allows to easily use
login forms. Once configured and added to an OpenerDirector, it recognizes
the login form and automatically sends the configured credentials.
It expects a session mechanism to keep track of the logged user.

## Installation

### Direct installation on Windows

Thanks to PyInstaller and InnoSetup, an installer and a portable zip file
are available on [Github](https://github.com/s-ball/qtimgren/releases).

That way you have no dependencies, not even on Python.

### From PyPI

    pip install qtimgren

### From Github

This is the recommended way if you want to contribute or simply tweak
`loginprocessor` to your own requirements. You can get a local copy by
downloading a zipfile but if you want to make changes, you should
 rather clone the repository to have access to all `git` goodies:

    git clone https://github.com/s-ball/loginprocessor.git

You can then install it in your main Python installation or in a venv with:

    pip install -e .

or on Windows with the launcher:

    py -m pip install -e .
    
Alternatively, you can use the `setup.py` script to build the unversioned
files without installing anything:

    python setup.py build

#### Special handling of `version.py`:

`loginprocessor` relies on `setuptools-scm` to automatically extract a
version number from git metadata and store it in a `version.py` file
for later use. The requires the availability of both `git` (which should
not be a problem when the project is downloaded from Github), and
`setuptools-scm`. If it fails because one is not available or because
git metadata is not there (if you only downloaded a zip archive from
Github), the version is set to 0.0.0

For that reason, if you do not use git to download the sources, you
should download a source distribution from PyPI, because the latter
contains a valid `version.py`

`pip` uses the `pyproject.toml` file with respect to PEP-518 and
PEP-517 to know that `setuptools-scm` is required before the build.

## Basic use

[Todo...]

## Contributions

Contributions are welcome, including translations or just issues on GitHub.
Problems are expected to be documented so that they can be reproduced. But
I only develop this on my free time, so I cannot guarantee quick answers...

## Disclaimer: beta quality

Despite an acceptable test coverage, this project still lacks a decent
documentation, and has not been extensively tested

## License

This work is licenced under a MIT Licence. See [LICENSE.txt](https://raw.githubusercontent.com/s-ball/MockSelector/master/LICENCE.txt)
