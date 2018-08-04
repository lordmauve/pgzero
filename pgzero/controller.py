import collections
import pygame
import pgzero.keyboard

from functools import partial

_pressed = set()
GAMEPADS = {
    0: {
        "id": 0,
        "keybindings": {
            "dpadleft": pygame.K_LEFT,
            "dpadright": pygame.K_RIGHT,
            "dpadup": pygame.K_UP,
            "dpaddown": pygame.K_DOWN,
        }
    },
    1: {
        "id": 1,
        "keybindings": {
            "dpadleft": pygame.K_a,
            "dpadright": pygame.K_d,
            "dpadup": pygame.K_w,
            "dpaddown": pygame.K_s,
        }
    },
}


def _joy_axis_release(joy=0, axis=0):
    dpads = ("dpadleft", "dpadright") if axis == 0 else ("dpadup", "dpaddown")
    option1 = GAMEPADS.get(joy, {}).get("keybindings", {}).get(dpads[0])
    option2 = GAMEPADS.get(joy, {}).get("keybindings", {}).get(dpads[1])
    if option1 in _pressed:
        return option1
    if option2 in _pressed:
        return option2
    return None


JoystickAxisEvent = collections.namedtuple(
    'JoystickAxisEvent',
    'type,joy,axis,value'
)

JOYSTICK_MAPPING = {
    # pressed
    # gamepad 0
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=0, value=-1
    ): GAMEPADS.get(0, {}).get("keybindings", {}).get("dpadleft"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=0, value=1
    ): GAMEPADS.get(0, {}).get("keybindings", {}).get("dpadright"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=1, value=-1
    ): GAMEPADS.get(0, {}).get("keybindings", {}).get("dpadup"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=1, value=1
    ): GAMEPADS.get(0, {}).get("keybindings", {}).get("dpaddown"),

    # gamepad 1
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=0, value=-1
    ): GAMEPADS.get(1, {}).get("keybindings", {}).get("dpadleft"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=0, value=1
    ): GAMEPADS.get(1, {}).get("keybindings", {}).get("dpadright"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=1, value=-1
    ): GAMEPADS.get(1, {}).get("keybindings", {}).get("dpadup"),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=1, value=1
    ): GAMEPADS.get(1, {}).get("keybindings", {}).get("dpaddown"),

    # released
    # gamepad 0
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=0, value=0
    ): partial(_joy_axis_release, joy=0, axis=0),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=0, axis=1, value=0
    ): partial(_joy_axis_release, joy=0, axis=1),

    # gamepad 1
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=0, value=0
    ): partial(_joy_axis_release, joy=1, axis=0),
    JoystickAxisEvent(
        type=pygame.JOYAXISMOTION, joy=1, axis=1, value=0
    ): partial(_joy_axis_release, joy=1, axis=1),
}


def initialize_joysticks():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print ("initializing joystick {}".format(joystick))
        joystick.init()


def _get_joy_event_elems(event):
    axis = getattr(event, 'axis', None)
    value = getattr(event, 'value', None)
    joy = getattr(event, 'joy', None)
    return axis, value, joy


def map_joy_event_key_down(event):
    axis, value, joy = _get_joy_event_elems(event)
    if value is None or not isinstance(value, float):
        return
    key = JOYSTICK_MAPPING.get((event.type, joy, axis, round(value)))
    if key:
        _pressed.add(key)
    return key


def map_joy_event_key_up(event):
    axis, value, joy = _get_joy_event_elems(event)
    if value is None or not isinstance(value, float):
        return
    partial_func = JOYSTICK_MAPPING.get((event.type, joy, axis, round(value)))
    key = partial_func() if callable(partial_func) else None
    if key:
        _pressed.remove(key)
    return key
