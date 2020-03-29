.. _install:

Installing alliancepy
=====================

Alliancepy can be installed with the Python package manager, `pip`. You can get either a stable release, or the development code directly from GitHub. You can also install with documentation packages if you are interested in helping develop the documentation, and you can install the async bundle for Asynchronous capabilities.

To install the stable release from PyPI:

.. code:: bash

	pip install alliancepy

To install the development version from GitHub:

.. code:: bash

	pip install https://github.com/karx1/alliancepy/archive/alliancepy.zip#egg=alliancepy

Both of the above methods support `extras`. These allow for extra functionality.
Simply append the name of the extra in brackets.

To install an extra, run:

.. code:: bash

	pip install <...>[name of extra]

Currently available is "docs", for helping develop the documentation, and "async", for Asynchronous capabilites.
