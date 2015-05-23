Installing Pygame Zero
======================

On OSX
~~~~~~

Homebrew
--------
homebrew_ is a package manager for OSX. It will allow you to install nearly everything you need to get Pygame Zero up and running.

Install homebrew_ using::
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Python3
------
As Pygame Zero is Python3 only you need to install python3.

Run::
    brew install python3

SDL
---
SDL is the graphics and sound library which Pygame uses. The following components are required for Pygame Zero to work correctly...

Run::
    brew install sdl sdl_mixer sdl_sound sdl_ttf

Pygame
------
Once the dependencies are installed pygame can be installed easily using Python's own package manager, pip3.

Run::
    pip3 install hg+http://bitbucket.org/pygame/pygame

Pygame Zero
-----------
Run::
    pip3 install pgzero

.. _homebrew: http://brew.sh/
