Pygame Zero
===========

A zero-boilerplate games programming framework based on Pygame.

Some examples
-------------

Pygame Zero consists of a runner ``pgzrun`` that will run a Pygame Zero script
with a full game loop and a range of useful builtins.

Here's some of the neat stuff you can do.

Draw graphics::

    def draw():
        screen.clear()
        screen.blit(images.dog, (10, 50))

Play a sound when you click the mouse::

    def on_mouse_down():
        sounds.eep.play()

Update and draw an "actor" object::

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

1. Install Pygame for Python 3
2. Install Pygame Zero (``python setup.py install``)
3. "python3 -m pgzero <pgzero program>" or (if installed correctly)
   ``pgzrun <program>``


Documentation
-------------

The full documentation is at http://pygame-zero.readthedocs.org/.

Read the tutorial at http://pygame-zero.readthedocs.org/en/latest/introduction.html
for a taste of the other things that Pygame Zero can do.
