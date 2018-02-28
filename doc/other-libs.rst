Other libraries like Pygame Zero
================================

Pygame Zero started a trend for Python "zero" libraries. Our friends have
created these great libraries. Some of these can be combined with Pygame Zero!


Network Zero
------------

`Network Zero`_ makes it simpler to have several machines or several processes
on one machine discovering each other and talking across a network.

.. caution::

    If you want to use Network Zero with Pygame Zero, make sure you don't let
    it **block** (stop everything while waiting for messages). This will
    interrupt Pygame Zero so that it stops animating the screen or even
    responding to input.  Always set the ``wait_for_s`` or ``wait_for_reply_s``
    options to ``0`` seconds.


.. _`Network Zero`: https://networkzero.readthedocs.io


GUI Zero
--------

`GUI Zero`_ is a library for creating Graphical User Interfaces (GUIs) with
windows, buttons, sliders, textboxes and so on.

Because GUI Zero and Pygame Zero both provide different approaches for drawing
to the screen, they are not usable together.


.. _`GUI Zero`: https://lawsie.github.io/guizero/


GPIO Zero
---------

`GPIO Zero`_ is a library for controlling devices connected to the General
Purpose Input/Output (GPIO) pins on a `Raspberry Pi`_.

GPIO Zero generally runs in its own thread, meaning that it will usually work
very well with Pygame Zero.

.. caution::

    When copying GPIO Zero examples, do not copy the ``time.sleep()`` function
    calls or ``while True:`` loops, as these will stop Pygame Zero animating
    the screen or responding to input. Use :ref:`clock` functions instead to
    call functions periodically, or the :func:`update()` function to check a
    value every frame.

.. _`GPIO Zero`: https://gpiozero.readthedocs.io/
.. _`Raspberry Pi`: https://www.raspberrypi.org/


Adventurelib
------------

`Adventurelib`_ is a library for creating making text-based games easier to
write (and which doesn't do everything for you!).

Writing text-based games requires a very different set of skills to writing
graphical games. Adventurelib is pitched at a slightly more advanced level of
Python programmer than Pygame Zero.

Adventurelib cannot currently be combined with Pygame Zero.


.. _Adventurelib: https://adventurelib.readthedocs.io/


.. tip::

    Know of another library that belongs here?

    `Open an issue <https://github.com/lordmauve/pgzero/issues/new>`_ on the
    issue tracker to let us know!
