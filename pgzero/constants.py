"""Names for constants returned by Pygame."""
from enum import IntEnum, Enum
import pygame.locals


# Event type indicating the end of a music track
MUSIC_END = 99


class mouse(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


class joysticks(IntEnum):
    JOYSTICK_1 = 0
    JOYSTICK_2 = 1


class joy_axis(IntEnum):
    VERTICAL = 1
    HORIZONTAL = 0


class joy_value(IntEnum):
    PRESSED_UP_OR_LEFT = -1
    PRESSED_DOWN_OR_RIGHT = 1
    RELEASED = 0


class joy_button(Enum):
    'simple snes joystick'
    BUTTON_A = "button_a"
    BUTTON_B = "button_b"
    BUTTON_X = "button_x"
    BUTTON_Y = "button_y"
    BUTTON_SELECT = "button_select"
    BUTTON_START = "button_start"
    BUTTON_RIGHT = "button_right"
    BUTTON_LEFT = "button_left"


# Use a code generation approach to copy Pygame's key constants out into
# a Python 3.4 IntEnum, stripping prefixes where possible
srclines = ["class keys(IntEnum):"]
for k, v in vars(pygame.locals).items():
    if k.startswith('K_'):
        if k[2].isalpha():
            k = k[2:]
        srclines.append("    %s = %d" % (k.upper(), v))

srclines.append("class keymods(IntEnum):")
for k, v in vars(pygame.locals).items():
    if k.startswith('KMOD_'):
        srclines.append("    %s = %d" % (k[5:].upper(), v))

exec('\n'.join(srclines), globals())
del srclines
