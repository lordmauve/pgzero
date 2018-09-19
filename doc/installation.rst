Installing Pygame Zero
======================

Included with Mu
----------------

The `Mu IDE <https://codewith.mu>`_, which is aimed at beginners, includes a
version of Pygame Zero.

You will need to `switch mode <https://codewith.mu/en/tutorials/1.0/modes>`_
into Pygame Zero mode to use it. Then type in a program and
`use the Play button <https://codewith.mu/en/tutorials/1.0/pgzero>`_ to run it
with Pygame Zero.

.. note::

    The version of Mu included with Pygame Zero may not be the latest version!
    You can find which version is installed by running this code in Mu::

        import pgzero
        print(pgzero.__version__)


Stand-alone installation
------------------------

First of all, you need **Python 3** installed! This is usually installed
already if you are using **Linux** or a **Raspberry Pi**. You can download it
from `python.org <https://www.python.org/>` on other systems.


Windows
'''''''

To install Pygame Zero, use **pip**. At a `command prompt`__, type

.. __: https://www.lifewire.com/how-to-open-command-prompt-2618089

::

    pip install pgzero


Mac
'''

In a Terminal window, type

::

   pip install pgzero


Note that there are currently no Wheels for Pygame that support python 3.4 for Mac,
so you may need to you will need to upgrade Python to >=3.6 (or use python 2.7) in
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


.. _install-repl:

Installing the REPL
-------------------

:doc:`Pygame Zero's REPL <repl>` is an optional feature. This can be enabled
when installing with ``pip`` by adding ``pgzero[repl]`` to the pip command
line::

    pip install pgzero[repl]

If you aren't sure if you have the REPL installed, you can still run this
command (it won't break anything if it is installed!).

