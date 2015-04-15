Event Hooks
===========

Pygame Zero will automatically pick up and call event hooks that you define.
This approach saves you from having to implement the event loop machinery
yourself.

Game Loop Hooks
---------------

A typical game loop looks a bit like this::

    while game_has_not_ended():
        process_input()
        update()
        draw()

Input processing is a bit more complicated, but Pygame Zero allows you to
easily define the ``update()`` and ``draw()`` functions within your game
module.

.. function:: draw()

    Called by Pygame Zero to redraw your game window.

    ``draw()`` must take no arguments.

.. function:: update() or update(dt)

    Called by Pygame Zero to step your game logic.

    There are two different approaches to writing an update function.

    In simple games you can assume a small time step (a fraction of a second)
    has elapsed between each call to ``update()``. Perhaps you don't even care
    how big that time step is: you can just move objects by a fixed number of
    pixels per frame (or accelerate them by a fixed constant, etc.)

    A more advanced approach is to base your movement and physics calculations
    on the actual amount of time that has elapsed between calls. This can give
    smoother animation, but the calculations involved can be harder and you
    must take more care to avoid unpredictable behaviour when the time steps
    grow larger.

    To use a time-based approach, you can change the update function to take a
    single parameter. If your update function takes an argument, Pygame Zero
    will pass it the elapsed time in seconds. You can use this to scale your
    movement calculations.


Event Handling Hooks
--------------------

Similar to the game loop hooks, your Pygame Zero program can respond to input
events by defining functions with specific names.

Somewhat like in the case of ``update()``, Pygame Zero will inspect your
event handler functions to determine how to call them. So you don't need to
make your handler functions take arguments. For example, Pygame Zero will
be happy to call any of these variations of an ``on_mouse_down`` function::

    def on_mouse_down():
        print("Mouse button clicked")

    def on_mouse_down(pos):
        print("Mouse button clicked at", pos)

    def on_mouse_down(button):
        print("Mouse button", button, "clicked")

    def on_mouse_down(pos, button):
        print("Mouse button", button, "clicked at", pos)

It does this by looking at the names of the parameters, so they must be spelled
exactly as above. Each event hook has a different set of parameters that you
can use, as described below.

.. function:: on_mouse_down([pos], [button])

    Called when a mouse button is depressed.

    :param pos: A tuple (x, y) that gives the location of the mouse pointer
                when the button was pressed.
    :param button: An integer indicating the button that was pressed (see
                   :ref:`below <buttons-and-keys>`).

.. function:: on_mouse_up([pos], [button])

    Called when a mouse button is released.

    :param pos: A tuple (x, y) that gives the location of the mouse pointer
                when the button was released.
    :param button: An integer indicating the button that was released (see
                   :ref:`below <buttons-and-keys>`).

.. function:: on_mouse_move([pos], [rel], [buttons])

    Called when the mouse is moved.

    :param pos: A tuple (x, y) that gives the location that the mouse pointer
                moved to.
    :param rel: A tuple (delta_x, delta_y) that represent the change in the
                mouse pointer's position.
    :param buttons: The buttons that were depressed, if any.


.. function:: on_key_down([key], [mod], [unicode])

    Called when a key is depressed.

    :param key: An integer indicating the key that was pressed (see
                :ref:`below <buttons-and-keys>`).
    :param unicode: Where relevant, the character that was typed. Not all keys
                    will result in printable characters - many may be control
                    characters. In the event that a key doesn't correspond to
                    a Unicode character, this will be the empty string.
    :param mod: A bitmask of modifier keys that were depressed.

.. function:: on_key_up([key], [mod])

    Called when a key is released.

    :param key: An integer indicating the key that was released (see
                :ref:`below <buttons-and-keys>`).
    :param mod: A bitmask of modifier keys that were depressed.


.. _buttons-and-keys:

Buttons and Keys
''''''''''''''''

Built-in objects ``mouse`` and ``keys`` can be used to determine which buttons
or keys were pressed in the above events.

Note that mouse scrollwheel events appear as button presses with the below
``WHEEL_UP``/``WHEEL_DOWN`` button constants.

.. class:: mouse

    A built-in enumeration of buttons that can be received by the
    ``on_mouse_*`` handlers.

    .. attribute:: LEFT
    .. attribute:: MIDDLE
    .. attribute:: RIGHT
    .. attribute:: WHEEL_UP
    .. attribute:: WHEEL_DOWN

.. class:: keys

    A built-in enumeration of keys that can be received by the ``on_key_*``
    handlers.

    .. attribute:: BACKSPACE
    .. attribute:: TAB
    .. attribute:: CLEAR
    .. attribute:: RETURN
    .. attribute:: PAUSE
    .. attribute:: ESCAPE
    .. attribute:: SPACE
    .. attribute:: EXCLAIM
    .. attribute:: QUOTEDBL
    .. attribute:: HASH
    .. attribute:: DOLLAR
    .. attribute:: AMPERSAND
    .. attribute:: QUOTE
    .. attribute:: LEFTPAREN
    .. attribute:: RIGHTPAREN
    .. attribute:: ASTERISK
    .. attribute:: PLUS
    .. attribute:: COMMA
    .. attribute:: MINUS
    .. attribute:: PERIOD
    .. attribute:: SLASH
    .. attribute:: K_0
    .. attribute:: K_1
    .. attribute:: K_2
    .. attribute:: K_3
    .. attribute:: K_4
    .. attribute:: K_5
    .. attribute:: K_6
    .. attribute:: K_7
    .. attribute:: K_8
    .. attribute:: K_9
    .. attribute:: COLON
    .. attribute:: SEMICOLON
    .. attribute:: LESS
    .. attribute:: EQUALS
    .. attribute:: GREATER
    .. attribute:: QUESTION
    .. attribute:: AT
    .. attribute:: LEFTBRACKET
    .. attribute:: BACKSLASH
    .. attribute:: RIGHTBRACKET
    .. attribute:: CARET
    .. attribute:: UNDERSCORE
    .. attribute:: BACKQUOTE
    .. attribute:: A
    .. attribute:: B
    .. attribute:: C
    .. attribute:: D
    .. attribute:: E
    .. attribute:: F
    .. attribute:: G
    .. attribute:: H
    .. attribute:: I
    .. attribute:: J
    .. attribute:: K
    .. attribute:: L
    .. attribute:: M
    .. attribute:: N
    .. attribute:: O
    .. attribute:: P
    .. attribute:: Q
    .. attribute:: R
    .. attribute:: S
    .. attribute:: T
    .. attribute:: U
    .. attribute:: V
    .. attribute:: W
    .. attribute:: X
    .. attribute:: Y
    .. attribute:: Z
    .. attribute:: DELETE
    .. attribute:: KP0
    .. attribute:: KP1
    .. attribute:: KP2
    .. attribute:: KP3
    .. attribute:: KP4
    .. attribute:: KP5
    .. attribute:: KP6
    .. attribute:: KP7
    .. attribute:: KP8
    .. attribute:: KP9
    .. attribute:: KP_PERIOD
    .. attribute:: KP_DIVIDE
    .. attribute:: KP_MULTIPLY
    .. attribute:: KP_MINUS
    .. attribute:: KP_PLUS
    .. attribute:: KP_ENTER
    .. attribute:: KP_EQUALS
    .. attribute:: UP
    .. attribute:: DOWN
    .. attribute:: RIGHT
    .. attribute:: LEFT
    .. attribute:: INSERT
    .. attribute:: HOME
    .. attribute:: END
    .. attribute:: PAGEUP
    .. attribute:: PAGEDOWN
    .. attribute:: F1
    .. attribute:: F2
    .. attribute:: F3
    .. attribute:: F4
    .. attribute:: F5
    .. attribute:: F6
    .. attribute:: F7
    .. attribute:: F8
    .. attribute:: F9
    .. attribute:: F10
    .. attribute:: F11
    .. attribute:: F12
    .. attribute:: F13
    .. attribute:: F14
    .. attribute:: F15
    .. attribute:: NUMLOCK
    .. attribute:: CAPSLOCK
    .. attribute:: SCROLLOCK
    .. attribute:: RSHIFT
    .. attribute:: LSHIFT
    .. attribute:: RCTRL
    .. attribute:: LCTRL
    .. attribute:: RALT
    .. attribute:: LALT
    .. attribute:: RMETA
    .. attribute:: LMETA
    .. attribute:: LSUPER
    .. attribute:: RSUPER
    .. attribute:: MODE
    .. attribute:: HELP
    .. attribute:: PRINT
    .. attribute:: SYSREQ
    .. attribute:: BREAK
    .. attribute:: MENU
    .. attribute:: POWER
    .. attribute:: EURO
    .. attribute:: LAST

Additionally you can access a set of constants that represent modifier keys:

.. class:: keymods

    Constants representing modifier keys that may have been depressed during
    an ``on_key_up``/``on_key_down`` event.

    .. attribute:: LSHIFT
    .. attribute:: RSHIFT
    .. attribute:: SHIFT
    .. attribute:: LCTRL
    .. attribute:: RCTRL
    .. attribute:: CTRL
    .. attribute:: LALT
    .. attribute:: RALT
    .. attribute:: ALT
    .. attribute:: LMETA
    .. attribute:: RMETA
    .. attribute:: META
    .. attribute:: NUM
    .. attribute:: CAPS
    .. attribute:: MODE

