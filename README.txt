Pygame Zero
===========

A zero-boilerplate games programming framework for Python 3, based on Pygame.

Some examples
-------------

Pygame Zero consists of a runner ``pgzrun`` that will run a Pygame Zero script
with a full game loop and a range of useful builtins.

Here's some of the neat stuff you can do. Note that each of these is a
self-contained script. There's no need for any imports or anything else in the
file.

Draw graphics (assuming there's  a file like ``images/dog.png`` or
``images/dog.jpg``)::

    def draw():
        screen.clear()
        screen.blit(images.dog, (10, 50))

Play the sound ``sounds/eep.wav`` when you click the mouse::

    def on_mouse_down():
        sounds.eep.play()

Draw an "actor" object (with the sprite ``images/alien.png``) that moves across
the screen::

    alien = Actor('alien')
    alien.pos = 10, 10

    def draw():
        screen.clear()
        alien.draw()

    def update():
        alien.x += 1
        if alien.left > WIDTH:
            alien.right = 0

Installation
------------

See `installation instructions`__.

.. __: http://pygame-zero.readthedocs.org/en/latest/installation.html


Documentation
-------------

The full documentation is at http://pygame-zero.readthedocs.org/.

Read the tutorial at http://pygame-zero.readthedocs.org/en/latest/introduction.html
for a taste of the other things that Pygame Zero can do.