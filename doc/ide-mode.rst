Running Pygame Zero in IDLE and other IDEs
==========================================

.. versionadded:: 1.2

Pygame Zero is usually run using a command such as::

    pgzrun my_program.py

Certain programs, such as integrated development environments like IDLE and
Edublocks, will only run ``python``, not ``pgzrun``.

Pygame Zero includes a way of writing a full Python program that can be run
using ``python``. To do it, put ::

    import pgzrun

as the very first line of the Pygame Zero program, and put ::

    pgzrun.go()

as the very last line.


Example
-------

Here is a Pygame Zero program that draws a circle. You can run this by pasting
it into IDLE::


    import pgzrun


    WIDTH = 800
    HEIGHT = 600

    def draw():
        screen.clear()
        screen.draw.circle((400, 300), 30, 'white')


    pgzrun.go()

