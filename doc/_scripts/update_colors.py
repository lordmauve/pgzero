"""Generate plots of the named colours, to include in docs."""
from pygame.colordict import THECOLORS
import colorsys
import numpy as np

OUT = 'colors_ref.rst'


def color_key(color_pair):
    """Generate a sort key for the given colour."""
    name, c = color_pair
    arr = np.array(c)
    h, s, v = colorsys.rgb_to_hsv(*arr[:3] / 255)
    return (s == 0, h, v, s)


def html_color(color):
    if len(color) == 3 or color[3] == 255:
        fmt = '#{:02x}{:02x}{:02x}'
    else:
        fmt = '#{:02x}{:02x}{:02x}{:02x}'

    return fmt.format(*color)


def hue_name(color):
    arr = np.array(color)
    h, s, v = colorsys.rgb_to_hsv(*arr[:3] / 255)
    if s == 0:
        return 'Greys'

    if h < 0.02:
        return 'Reds'
    elif h < 0.11:
        return "Oranges"
    elif h < 0.2:
        return "Yellows"
    elif h < 0.45:
        return "Greens"
    elif h < 0.52:
        return "Turquoises"
    elif h < 0.7:
        return "Blues"
    else:
        return "Purples"


def simplified_color_table():
    """De-dupe the colour table."""
    by_hex = {}

    for name, color in THECOLORS.items():
        if name[-1].isdigit():
            continue
        html = html_color(color)
        by_hex.setdefault(html, []).append(name)

    return {
        ' / '.join(sorted(names)): THECOLORS[names[0]]
        for names in by_hex.values()
    }


SIMPLE_COLORS = simplified_color_table()
omitted_colors = sorted(THECOLORS.keys() - SIMPLE_COLORS.keys())
some_color = omitted_colors[0]


def gen_table(f):
    colors = list(SIMPLE_COLORS.items())
    colors.sort(key=color_key)

    last_hue = None

    for name, color in colors:
        html = html_color(color)

        arr = np.array(color) / 255
        rgb = arr[:3]
        a = arr[3]
        effective_rgb = rgb * a + (1 - a) * np.ones(3)

        lum = np.dot(
            effective_rgb,
            [0.3, 0.6, 0.1]
        )
        if lum > 0.5:
            font = 'black'
        else:
            font = 'white'

        darker = html_color((effective_rgb * 128).astype(np.uint8))

        hue = hue_name(color)

        if hue != last_hue:
            print(file=f)
            print(hue, file=f)
            print('-' * len(hue), file=f)
            print(file=f)
            last_hue = hue

        print("""\
.. raw:: html

    <div class="color-swatch"
         style="color: {font}; background-color: {hex};
                border-color: {darker}">
        {name}<br>
        <code>{hex}</code>
    </div>

""".format(name=name, hex=html, font=font, darker=darker), file=f)


if __name__ == '__main__':
    with open(OUT, 'w') as f:
        print("""\
:orphan:

Pygame Colors
=============

Below is a list of the {} colour names supported in Pygame [1]_ .

""".format(len(SIMPLE_COLORS)), file=f)
        gen_table(f)
        print("""\

.. [1] In fact, many of these names have additional fine variations with
       digits appended, eg. ``{}``. Because the differences are small, and
       there are so many colours without these, these variants have been
       omitted here.
""".format(some_color), file=f)
