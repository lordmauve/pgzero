Text Formatting
---------------

The :ref:`screen`'s ``draw.text()`` method has a very rich set of methods for
position and formatting of text. Some examples::

    screen.draw.text("Text color", (50, 30), color="orange")
    screen.draw.text("Font name and size", (20, 100), fontname="boogaloo", fontsize=60)
    screen.draw.text("Positioned text", topright=(840, 20))
    screen.draw.text("Allow me to demonstrate wrapped text.", (90, 210), width=180, lineheight=1.5)
    screen.draw.text("Outlined text", (400, 70), owidth=1.5, ocolor=(255,255,0), color=(0,0,0))
    screen.draw.text("Drop shadow", (640, 110), shadow=(2,2), scolor="#202020")
    screen.draw.text("Color gradient", (540, 170), color="red", gcolor="purple")
    screen.draw.text("Transparency", (700, 240), alpha=0.1)
    screen.draw.text("Vertical text", midleft=(40, 440), angle=90)
    screen.draw.text("All together now:\nCombining the above options",
        midbottom=(427,460), width=360, fontname="boogaloo", fontsize=48,
        color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8)

In its simplest usage, ``screen.draw.text`` requires the string you want to
draw, and the position. You can either do this by passing coordinates as the
second argument (which is the top left of where the text will appear), or use
the positioning keyword arguments (described later)::

    screen.draw.text("hello world", (20, 100))

``screen.draw.text`` takes many optional keyword arguments, described below.

Font name and size
''''''''''''''''''

Fonts are loaded from a directory named ``fonts``, in a similar way to the
handling of images and sounds. Fonts must be in ``.ttf`` format. For example::

    screen.draw.text("hello world", (100, 100), fontname="Viga", fontsize=32)

Keyword arguments:

-  ``fontname``: filename of the font to draw. By default, use the system font.
-  ``fontsize``: size of the font to use, in pixels. Defaults to ``24``.
-  ``antialias``: whether to render with antialiasing. Defaults to ``True``.

Color and background color
''''''''''''''''''''''''''

::

    screen.draw.text("hello world", (100, 100), color=(200, 200, 200), background="gray")

Keyword arguments:

-  ``color``: foreground color to use. Defaults to ``white``.
-  ``background``: background color to use. Defaults to ``None``.

``color`` (as well as ``background``, ``ocolor``, ``scolor``, and
``gcolor``) can be an (r, g, b) sequence such as ``(255,127,0)``, a
``pygame.Color`` object, a color name such as ``"orange"``, an HTML hex
color string such as ``"#FF7F00"``, or a string representing a hex color
number such as ``"0xFF7F00"``.

``background`` can also be ``None``, in which case the background is
transparent. Unlike ``pygame.font.Font.render``, it's generally not more
efficient to set a background color when calling ``screen.draw.text``. So only
specify a background color if you actually want one.

Colors with alpha transparency are not supported (except for the special
case of invisible text with outlines or drop shadows - see below). See
the ``alpha`` keyword argument for transparency.

Positioning
'''''''''''

::

    screen.draw.text("hello world", centery=50, right=300)
    screen.draw.text("hello world", midtop=(400, 0))

Keyword arguments:

::

    top left bottom right
    topleft bottomleft topright bottomright
    midtop midleft midbottom midright
    center centerx centery

Positioning keyword arguments behave like the corresponding properties
of ``pygame.Rect``. Either specify two arguments, corresponding to the
horizontal and vertical positions of the box, or a single argument that
specifies both.

If the position is overspecified (e.g. both ``left`` and ``right`` are
given), then extra specifications will be (arbitrarily but
deterministically) discarded. For constrained text, see the section on
``screen.draw.textbox`` below.

Word wrap
'''''''''

::

    screen.draw.text("splitting\nlines", (100, 100))
    screen.draw.text("splitting lines", (100, 100), width=60)

Keyword arguments:

-  ``width``: maximum width of the text to draw, in pixels. Defaults to
   ``None``.
-  ``widthem``: maximum width of the text to draw, in font-based em
   units. Defaults to ``None``.
-  ``lineheight``: vertical spacing between lines, in units of the
   font's default line height. Defaults to ``1.0``.

``screen.draw.text`` will always wrap lines at newline (``\n``) characters. If
``width`` or ``widthem`` is set, it will also try to wrap lines in order
to keep each line shorter than the given width. The text is not
guaranteed to be within the given width, because wrapping only occurs at
space characters, so if a single word is too long to fit on a line, it
will not be broken up. Outline and drop shadow are also not accounted
for, so they may extend beyond the given width.

You can prevent wrapping on a particular space with non-breaking space
characters (``\u00A0``).

Text alignment
''''''''''''''

::

    screen.draw.text("hello\nworld", bottomright=(500, 400), align="left")

Keyword argument:

-  ``align``: horizontal positioning of lines with respect to each
   other. Defaults to ``None``.

``align`` determines how lines are positioned horizontally with respect
to each other, when more than one line is drawn. Valid values for
``align`` are the strings ``"left"``, ``"center"``, or ``"right"``, a
numerical value between ``0.0`` (for left alignment) and ``1.0`` (for
right alignment), or ``None``.

If ``align`` is ``None``, the alignment is determined based on other arguments,
in a way that should be what you want most of the time. It depends on any
positioning arguments (``topleft``, ``centerx``, etc.), ``anchor``, and finally
defaults to ``"left"``. I suggest you generally trust the default alignment,
and only specify ``align`` if something doesn't look right.

Outline
'''''''

::

    screen.draw.text("hello world", (100, 100), owidth=1, ocolor="blue")

Keyword arguments:

-  ``owidth``: outline thickness, in outline units. Defaults to
   ``None``.
-  ``ocolor``: outline color. Defaults to ``"black"``.

The text will be outlined if ``owidth`` is specified. The outlining is a
crude manual method, and will probably look bad at large sizes. The
units of ``owidth`` are chosen so that ``1.0`` is a good typical value
for outlines. Specifically, they're the font size divided by 24.

As a special case, setting ``color`` to a transparent value (e.g.
``(0,0,0,0)``) while using outilnes will cause the text to be invisible,
giving a hollow outline. (This feature is not compatible with
``gcolor``.)

Valid values for ``ocolor`` are the same as for ``color``.

Drop shadow
'''''''''''

::

    screen.draw.text("hello world", (100, 100), shadow=(1.0,1.0), scolor="blue")

Keyword arguments:

-  ``shadow``: (x,y) values representing the drop shadow offset, in
   shadow units. Defaults to ``None``.
-  ``scolor``: drop shadow color. Defaults to ``"black"``.

The text will have a drop shadow if ``shadow`` is specified. It must be
set to a 2-element sequence representing the x and y offsets of the drop
shadow, which can be positive, negative, or 0. For example,
``shadow=(1.0,1.0)`` corresponds to a shadow down and to the right of
the text. ``shadow=(0,-1.2)`` corresponds to a shadow higher than the
text.

The units of ``shadow`` are chosen so that ``1.0`` is a good typical
value for the offset. Specifically, they're the font size divided by 18.

As a special case, setting ``color`` to a transparent value (e.g.
``(0,0,0,0)``) while using drop shadow will cause the text to be
invisible, giving a hollow shadow. (This feature is not compatible with
``gcolor``.)

Valid values for ``scolor`` are the same as for ``color``.

Gradient color
''''''''''''''

::

    screen.draw.text("hello world", (100, 100), color="black", gcolor="green")

Keyword argument:

-  ``gcolor``: Lower gradient stop color. Defaults to ``None``.

Specify ``gcolor`` to color the text with a vertical color gradient. The
text's color will be ``color`` at the top and ``gcolor`` at the bottom.
Positioning of the gradient stops and orientation of the gradient are
hard coded and cannot be specified.


Alpha transparency
''''''''''''''''''

::

    screen.draw.text("hello world", (100, 100), alpha=0.5)

Keyword argument:

-  ``alpha``: alpha transparency value, between 0 and 1. Defaults to
   ``1.0``.

In order to maximize reuse of cached transparent surfaces, the value of
``alpha`` is rounded.


Anchored positioning
''''''''''''''''''''

::

    screen.draw.text("hello world", (100, 100), anchor=(0.3,0.7))

Keyword argument:

-  ``anchor``: a length-2 sequence of horizontal and vertical anchor
   fractions. Defaults to ``(0.0, 0.0)``.

``anchor`` specifies how the text is anchored to the given position,
when no positioning keyword arguments are passed. The two values in
``anchor`` can take arbitrary values between ``0.0`` and ``1.0``. An
``anchor`` value of ``(0,0)``, the default, means that the given
position is the top left of the text. A value of ``(1,1)`` means the
given position is the bottom right of the text.

Rotation
''''''''

::

    screen.draw.text("hello world", (100, 100), angle=10)

Keyword argument:

-  ``angle``: counterclockwise rotation angle in degrees. Defaults to
   ``0``.

Positioning of rotated surfaces is tricky. When drawing rotated text, the
anchor point, the position you actually specify, remains fixed, and the text
rotates around it. For instance, if you specify the top left of the text to be
at ``(100, 100)`` with an angle of ``90``, then the Surface will actually be
drawn so that its bottom left is at ``(100, 100)``.

If you find that confusing, try specifying the center. If you anchor the
text at the center, then the center will remain fixed, no matter how you
rotate it.

In order to maximize reuse of cached rotated surfaces, the value of
``angle`` is rounded to the nearest multiple of 3 degrees.


Constrained text
''''''''''''''''

::

    screen.draw.textbox("hello world", (100, 100, 200, 50))

``screen.draw.textbox`` requires two arguments: the text to be drawn, and a
``pygame.Rect`` or a ``Rect``-like object to stay within. The font size
will be chosen to be as large as possible while staying within the box.
Other than ``fontsize`` and positional arguments, you can pass all the
same keyword arguments to ``screen.draw.textbox`` as to ``screen.draw.text``.
