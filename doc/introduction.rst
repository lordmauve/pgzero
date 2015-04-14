Introduction to Pygame Zero
===========================

Creating a window
-----------------

First, create an empty file called "intro.py".

Verify that this runs and creates a blank window by running ::

    pgzrun intro.py

Everything in Pygame Zero is optional; a blank file is a valid Pygame Zero
script!


Drawing a background
--------------------

Next, let's add a ``draw()`` function. Pygame Zero will call this function
whenever it needs to paint the screen.

In ``intro.py``, add the following::

    def draw():
        screen.fill((128, 0, 0))

Re-run ``pgzrun intro.py`` and the screen should now be filled with red!

What is this code doing?

In Pygame Zero, ``screen`` is a built-in that represents the window display. It
is technically an instance of a `Pygame Surface`_, which means it has methods
like ``.fill()``, which take an RGB color triple.

.. _`Pygame Surface`: https://www.pygame.org/docs/ref/surface.html


Handling clicks
---------------

Let's add a little event handling. Change ``intro.py`` to read::

    bg = [150, 0, 80]

    def draw():
        screen.fill(bg)

    def on_mouse_down():
        bg.insert(0, bg.pop())

Now, when you click on the window, the colours will change! We are using the
``.insert()`` and ``.pop()`` methods of a list to mutate ``bg`` in place.


Diversion: Local and Global Variables
-------------------------------------

Suppose we wrote the following code::

    RED = 150, 0, 0
    GREEN = 0, 128, 0

    bg = RED

    def draw():
        screen.fill(bg)

    def on_mouse_down():
        bg = GREEN

    def on_mouse_up():
        bg = RED

In some languages, this would work: the screen would change to green
when the mouse button was pressed, and change back to red when the button is
released.

This code doesn't work in Python. If you try it, you will not see the screen
change to green. Why?

When you assign with the ``=`` operator inside a function, you create a "local"
variable called ``bg`` that exists only with the function. The ``bg`` we want
to change is in the global scope.

The fix is to declare in ``on_mouse_down()`` and ``on_mouse_up()`` that we
want to modify the global variable, not create a new local variable. We do
this with the ``global`` statement. The correct code in Pygame Zero is::

    RED = 150, 0, 0
    GREEN = 0, 128, 0

    bg = RED

    def draw():
        screen.fill(bg)

    def on_mouse_down():
        global bg
        bg = GREEN

    def on_mouse_up():
        global bg
        bg = RED
