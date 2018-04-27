Roadmap
=======

Pygame Zero is an open source project, and as with any such project, the
development roadmap is subject to change.

This document just lays out some goals for future releases, but there is **no
guarantee** that these targets will be hit.


Translations
------------

Pygame Zero is aimed at young users, whose English skills might not be good
enough to read the documentation if it isn't in their own language.

Adding translations of the documentation would help to bring Pygame Zero to new
users. This is something that needs contributors to help with. My own language
skills aren't good enough!

Please see :ref:`the translating guide <translating>` if you think you can
help.


Gamepad Support
---------------

Github Issue: `#70 <https://github.com/lordmauve/pgzero/issues/70>`_

SNES-style gamepads are now extremely cheap. For example, they are sold for
a few pounds from the `Pi Hut`_, in packs of 2 at Amazon_, and even in some
Raspberry Pi bundles.

Gamepad support should not be limited to these specific models; rather, we
should treat this as a lowest-common-denominator across modern gamepads, as
nearly all more modern gamepads have at least as many buttons and axes.

This feature needs to be added in a way that will not **require** a gamepad to
play any Pygame Zero game, in order to follow the principle of
:ref:`accessibility`.

.. _`Pi Hut`: https://thepihut.com/products/raspberry-pi-compatible-usb-gamepad-controller-snes-style
.. _Amazon: https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Delectronics&field-keywords=usb+snes


REPL
----

Python's REPL is a valuable feature that makes the language much more
accessible to beginners.

Python programs that present a user interface, however, rarely provide a REPL,
because the main thread is used to run the event loop for the user interface.

However, Javascript in a web browser demonstrates how this can work. You have
access to an interactive REPL that allows investigating program state *while
you interact with the interface*. This is very useful for debugging, and would
be a powerful addition to Pygame Zero.


Surface juggling
----------------

Github Issue: `#71 <https://github.com/lordmauve/pgzero/issues/71>`_

Pygame experts make lots of use of off-screen surfaces to create interesting
effects.

Pygame Zero chose to consider only the screen surface, which we wrap with
a richer ``Screen`` API for drawing, etc.

The problem is that there is no easy path to using additional surfaces -
Pygame Zero immediately becomes dead weight as you start to look past that
curtain.

We should look to smooth out this path to make Pygame Zero Actors and Screen
work better with custom surfaces.


Storage
-------

Github Issue: `#33 <https://github.com/lordmauve/pgzero/issues/33>`_

It would be useful for users to be able to save and load data.

The obvious application is save games, but saving and loading whole games can
be pretty hard to get right. The simpler application would just be saving
settings, customisations, high scores, or the highest level reached.

Python of course has APIs for reading and writing files, but this has
additional complexity that teachers might not want to teach immediately.
