Contributing to Pygame Zero
===========================

The Pygame Zero project is hosted on bitbucket:

    https://bitbucket.org/lordmauve/pgzero

Development installation
------------------------

It's possible to create a locally-editable install using pip. From the root directory of the checked out source, run::

    pip3 install --editable .

The installed version will now reflect any local changes you make.

Alternatively, if you don't want to install it at all, it may be run with:

   python3 -m pgzero <name of pgzero script>

For example:

   python3 -m pgzero examples/basic/demo1.py

Tests
-----

The tests can be run with

    python3 setup.py test
