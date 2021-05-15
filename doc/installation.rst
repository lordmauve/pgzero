Installing Pygame Zero
======================

On desktop systems
~~~~~~~~~~~~~~~~~~

::

    pip install pgzero

This will also install Pygame. Pre-compiled Pygame packages are available to pip
for Windows & Linux (32-bit and 64-bit), and for Mac OS (64-bit only). If you
have a different system, you'll need to find a way to install pygame first. Make
sure you are using Python 3 not Python 2.

Mac
'''

In a Terminal window, type

::

   pip install pgzero


Note that there are currently no Wheels for Pygame that support python 3.4 for Mac,
so you will need to upgrade Python to >=3.6 (or use python 2.7) in
order to be able to install pygame. For a list of available Wheels, please visit
`pyPI_`

.. _pyPI: https://pypi.org/project/Pygame/#files

Linux
'''''

In a terminal window, type

::

   sudo pip install pgzero


Some Linux systems call it ``pip3``; if the above command printed something
like ``sudo: pip: command not found`` then try::

    sudo pip3 install pgzero

Sometimes pip is not installed and needs to be installed. If so try this before
running the above commands again::


    sudo python3 -m ensurepip


On Raspberry Pi
~~~~~~~~~~~~~~~

pgzero has been installed by default since the release of Raspbian Jessie in
September 2015!
