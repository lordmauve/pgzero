"""Names for constants returned by Pygame."""
from enum import IntEnum
import pygame.locals


# Event type indicating the end of a music track
MUSIC_END = 99


class mouse(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


class joybtn(IntEnum):
    NUM = 16
    FACE_UP = 0
    FU = 0
    FACE_DOWN = 1
    FD = 1
    FACE_LEFT = 2
    FL = 2
    FACE_RIGHT = 3
    FR = 3
    DPAD_UP = 4
    DU = 4
    DPAD_DOWN = 5
    DD = 5
    DPAD_LEFT = 6
    DL = 6
    DPAD_RIGHT = 7
    DR = 7
    SHOULDER_LEFT = 8
    SL = 8
    SHOULDER_RIGHT = 9
    SR = 9
    PUSH_LEFT = 10
    PL = 10
    PUSH_RIGHT = 11
    PR = 11
    CENTER_LEFT = 12
    CL = 12
    CENTER_MIDDLE = 13
    CM = 13
    CENTER_RIGHT = 14
    CR = 14
    UNKNOWN = 15


class axis(IntEnum):
    NUM = 7
    LEFT_X = 0
    LX = 0
    LEFT_Y = 1
    LY = 1
    LEFT_TRIGGER = 2
    LT = 2
    RIGHT_X = 3
    RX = 3
    RIGHT_Y = 4
    RY = 4
    RIGHT_TRIGGER = 5
    RT = 5
    UNKNOWN = 6


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
