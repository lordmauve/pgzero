Introduction to Pygame Zero
===========================

.. highlight:: python
    :linenothreshold: 5

Creating a window
-----------------

First, create an empty file called ``intro.py``.

Verify that this runs and creates a blank window by running ::

    pgzrun intro.py

Everything in Pygame Zero is optional; a blank file is a valid Pygame Zero
script!

You can quit the game by clicking on the window's close button or by pressing
``Ctrl-Q`` (``⌘-Q`` on Mac). If the game stops responding for any reason, you
may need to terminate it by pressing ``Ctrl-C`` in your Terminal window.


Drawing a background
--------------------

Next, let's add a :func:`draw` function. Pygame Zero will call this function
whenever it needs to paint the screen.

In ``intro.py``, add the following::

    WIDTH = 300
    HEIGHT = 300

    def draw():
        screen.fill((128, 0, 0))

Re-run ``pgzrun intro.py`` and the screen should now be a reddish square!

What is this code doing?

``WIDTH`` and ``HEIGHT`` control the width and height of your window. The code
sets the window size to be 300 pixels in each dimension.

``screen`` is a built-in that represents the window display. It has a
:ref:`range of methods for drawing sprites and shapes <screen>`. The
``screen.fill()`` method call is filling the screen with a solid colour,
specified as a ``(red, green, blue)`` colour tuple. ``(128, 0, 0)`` will be a
medium-dark red.

Pygame Zero is actually calling your draw function many times a second. If your
``draw()`` function draws slightly different things every frame, it will appear
as an animation. We'll explore this shortly. For now, let's set up a sprite
that we can animate.


Draw a sprite
-------------

Before we can draw anything, we'll need to save an alien sprite to use. You can
right click on this one and save it ("Save Image As..." or similar).

.. image:: _static/alien.png

(This sprite has a transparency (or "alpha") channel, which is great for games!
But it's designed for a dark background, so you may not be able to see the
alien's space helmet until it is shown in the game).

You need to save the file in the right place so that Pygame Zero can find it.
Create a directory called ``images`` and save the image into it as
``alien.png``. Both of those must be lower case. Pygame Zero will complain
otherwise, to alert you to a potential cross-platform compatibility pitfall.

If you've done that, your project should look like this::

    .
    ├── images/
    │   └── alien.png
    └── intro.py

``images/`` is the standard directory that Pygame Zero will look in to find
your images.

There's a built-in class called :class:`Actor` that you can use to represent a
graphic to be drawn to the screen.

Let's define one now. Change the ``intro.py`` file to read::

    alien = Actor('alien')
    alien.pos = 100, 56

    WIDTH = 500
    HEIGHT = alien.height + 20

    def draw():
        screen.clear()
        alien.draw()

Your alien should now be appearing on screen! By passing the string ``'alien'``
to the ``Actor`` class, it automatically loads the sprite, and has attributes
like positioning and dimensions. This allows us to set the ``HEIGHT`` of
the window based on the height of the alien.

The ``alien.draw()`` method draws the sprite to the screen at its current
position.

Moving the alien
----------------

Let's set the alien off-screen; change the ``alien.pos`` line to read::

    alien.topright = 0, 10

Note how you can assign to ``topright`` to move the alien actor by its
top-right corner. If the right-hand edge of the alien is at ``0``, the the
alien is just offscreen to the left.  Now let's make it move. Add the following
code to the bottom of the file::

    def update():
        alien.left += 2
        if alien.left > WIDTH:
            alien.right = 0

Pygame Zero will call your :func:`update` function once every frame. Moving the
alien a small number of pixels every frame will cause it to slide across the
screen. Once it slides off the right-hand side of the screen, we reset it back
to the left.

Handling clicks
---------------

Let's make the game do something when you click on the alien. To do this we
need to define a function called :func:`on_mouse_down`. Add this to the source
code::

    def on_mouse_down(pos):
        if alien.collidepoint(pos):
            print("Eek!")
        else:
            print("You missed me!")

You should run the game and try clicking on and off the alien.

Pygame Zero is smart about how it calls your functions. If you don't define
your function to take a ``pos`` parameter, Pygame Zero will call it without
a position. There's also a ``button`` parameter for ``on_mouse_down``. So we
could have written::

    def on_mouse_down():
        print("You clicked!")

or::

    def on_mouse_down(pos, button):
        if button == mouse.LEFT and alien.collidepoint(pos):
            print("Eek!")


Sounds and images
-----------------

Now let's make the alien appear hurt. Save these files:

* `alien_hurt.png <_static/alien_hurt.png>`_ - save this as ``alien_hurt.png``
  in the ``images`` directory.
* `eep.wav <_static/eep.wav>`_ - create a directory called ``sounds`` and save
  this as ``eep.wav`` in that directory.

Your project should now look like this::

    .
    ├── images/
    │   └── alien.png
    ├── sounds/
    │   └── eep.wav
    └── intro.py

``sounds/`` is the standard directory that Pygame Zero will look in to find
your sound files.

Now let's change the ``on_mouse_down`` function to use these new resources::

    def on_mouse_down(pos):
        if alien.collidepoint(pos):
            sounds.eep.play()
            alien.image = 'alien_hurt'

Now when you click on the alien, you should hear a sound, and the sprite will
change to an unhappy alien.

There's a bug in this game though; the alien doesn't ever change back to a
happy alien (but the sound will play on each click). Let's fix this next.


Clock
-----

If you're familiar with Python outside of games programming, you might know the
``time.sleep()`` method that inserts a delay. You might be tempted to write
code like this::

    def on_mouse_down(pos):
        if alien.collidepoint(pos):
            sounds.eep.play()
            alien.image = 'alien_hurt'
            time.sleep(1)
            alien.image = 'alien'

Unfortunately, this is not at all suitable for use in a game. ``time.sleep()``
blocks all activity; we want the game to go on running and animating. In fact
we need to return from ``on_mouse_down``, and let the game work out when to
reset the alien as part of its normal processing, all the while running your
``draw()`` and ``update()`` methods.

This is not difficult with Pygame Zero, because it has a built-in
:class:`Clock` that can schedule functions to be called later.

First, let's "refactor" (ie. re-organise the code). We can create functions to
set the alien as hurt and also to change it back to normal::

    def on_mouse_down(pos):
        if alien.collidepoint(pos):
            set_alien_hurt()


    def set_alien_hurt():
        alien.image = 'alien_hurt'
        sounds.eep.play()


    def set_alien_normal():
        alien.image = 'alien'

This is not going to do anything different yet. ``set_alien_normal()`` won't be
called. But let's change ``set_alien_hurt()`` to use the clock, so that the
``set_alien_normal()`` will be called a little while after. ::

    def set_alien_hurt():
        alien.image = 'alien_hurt'
        sounds.eep.play()
        clock.schedule_unique(set_alien_normal, 1.0)

``clock.schedule_unique()`` will cause ``set_alien_normal()`` to be called
after ``1.0`` second. ``schedule_unique()`` also prevents the same function
being scheduled more than once, such as if you click very rapidly.

Try it, and you'll see the alien revert to normal after 1 second. Try clicking
rapidly and verify that the alien doesn't revert until 1 second after the last
click.


Summary
-------

We've seen how to load and draw sprites, play sounds, handle input events, and
use the built-in clock.

You might like to expand the game to keep score, or make the alien move more
erratically.

There are lots more features built in to make Pygame Zero easy to use. Check
out the :doc:`built in objects <builtins>` to learn how to use the rest of the
API.
