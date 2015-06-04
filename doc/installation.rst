Installing Pygame Zero
======================

On Windows
~~~~~~~~~~

1. Install Pygame for Python 3. This is available as a .msi installer from the
   `Pygame Bitbucket`_.
2. Install Pygame Zero with pip::

    pip install pgzero

.. _`Pygame Bitbucket`: https://bitbucket.org/pygame/pygame/downloads


On OSX
~~~~~~

homebrew_ is a package manager for OSX. It will allow you to install nearly
everything you need to get Pygame Zero up and running.

All commands will be entered in a Terminal window.

1. Install homebrew_::

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. Install Python 3::

    brew install python3

3. Install the following dependencies, needed for compiling Pygame::

    brew install sdl sdl_mixer sdl_sound sdl_ttf

4. Now pygame can be installed easily using Python's own package manager,
   pip3::

    pip3 install hg+http://bitbucket.org/pygame/pygame

5. Finally, install Pygame Zero! ::

    pip3 install pgzero

.. _homebrew: http://brew.sh/


On Ubuntu Linux
~~~~~~~~~~~~~~~

There is a .deb package of Pygame for Python 3 available in `this PPA`__.

.. __: https://launchpad.net/~thopiekar/+archive/ubuntu/pygame

1. Add the PPA to your system sources::

    sudo add-apt-repository ppa:thopiekar/pygame

2. Update the package list::

    sudo apt-get update

3. Install the package::

    sudo apt-get install python3-pygame

2. Install Pygame Zero with pip::

    pip3 install pgzero

On Debian 8 (Jessie)
~~~~~~~~~~~~~~~~~~~~

(There is a .deb package of Pygame for Python 3 in Debian unstable "Sid". On
Jessie it's relatively simply to compile Pygame yourself.)

1. Install the dependencies::

    sudo apt-get install mercurial python3-dev python3-numpy libav-tools \
        libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
        libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev \
        libavcodec-dev build-essential

2. Grab Pygame source::

    hg clone https://bitbucket.org/pygame/pygame

3. Build Pygame::

    cd pygame
    python3 setup.py build

4. Install Pygame::

    sudo python3 setup.py install

5. Install Pygame Zero with pip::

    pip3 install pgzero

On Raspberry Pi
~~~~~~~~~~~~~~~

pgzero is likely to make an appearance in the Raspbian repo before long;
until then...

(Starting from a vanilla noobs-install Raspbian)

1. sudo apt-get update

2. sudo apt-get install python3-setuptools python3-pip

3. sudo pip-3.2 install pgzero

