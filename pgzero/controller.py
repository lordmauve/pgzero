import collections
import numbers
import functools

import pygame

import pgzero.keyboard

_pressed = set()
JOYSTICKS = {
    0: {
        "id": 0,
        "keybindings": {
            "dpadleft": pygame.K_LEFT,
            "dpadright": pygame.K_RIGHT,
            "dpadup": pygame.K_UP,
            "dpaddown": pygame.K_DOWN,
            0: pygame.K_LEFTBRACKET,
            3: pygame.K_RETURN,
            1: pygame.K_RIGHTBRACKET,
            2: pygame.K_BACKSLASH,
        }
    },
    1: {
        "id": 1,
        "keybindings": {
            "dpadleft": pygame.K_a,
            "dpadright": pygame.K_d,
            "dpadup": pygame.K_w,
            "dpaddown": pygame.K_s,
            0: pygame.K_v,
            3: pygame.K_SPACE,
            1: pygame.K_b,
            2: pygame.K_n,
        }
    },
}


def _joy_axis_release(joy=0, axis=0):
    # joy axis release events are the same for right&left or up&down
    # so look into _pressed set to see what was previously pressed.
    # but be wary:
    #  on joystick initialize the 'release' events for both axes are sent
    # TODO: we might want to not add those events to _pressed set
    dpads = ("dpadleft", "dpadright") if axis == 0 else ("dpadup", "dpaddown")
    option1 = JOYSTICKS.get(joy, {}).get("keybindings", {}).get(dpads[1])
    option2 = JOYSTICKS.get(joy, {}).get("keybindings", {}).get(dpads[0])
    if option1 in _pressed:
        return option1
    if option2 in _pressed:
        return option2
    return None


JoystickAxisEvent = collections.namedtuple(
    'JoystickAxisEvent',
    'type,joy,axis,value'
)
JoystickButtonEvent = collections.namedtuple(
    'JoystickButtonEvent',
    'type,joy,button'
)


def one_joystick_mapping(joystick):
    """ map joystick events from a single joystick to JOYSTICKS keybindings."""
    return {
        # pressed events
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=0, value=-1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get("dpadleft"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=0, value=1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get("dpadright"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=1, value=-1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get("dpadup"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=1, value=1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get("dpaddown"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joystick, button=0
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(0),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joystick, button=1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(1),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joystick, button=2
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(2),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joystick, button=3
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(3),
        # release events
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=0, value=0
        ): functools.partial(_joy_axis_release, joy=joystick, axis=0),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joystick, axis=1, value=0
        ): functools.partial(_joy_axis_release, joy=joystick, axis=1),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joystick, button=0
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(0),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joystick, button=1
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(1),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joystick, button=2
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(2),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joystick, button=3
        ): JOYSTICKS.get(joystick, {}).get("keybindings", {}).get(3),
    }


def build_joystick_mapping():
    """ build a dictionary with josytick events mapped to pygame keys.
        uses JOYSTICKS as basis."""
    result = {}
    for joystick in JOYSTICKS.keys():
        result.update(one_joystick_mapping(joystick))
    return result


JOYSTICK_MAPPING = build_joystick_mapping()


def initialize_joysticks():
    """ initialize pygame.joystick module,
        and call init on available joysticks."""
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print ("initializing joystick {}".format(joystick))
        joystick.init()


def quit_joysticks():
    """ deinit (only) initialized joysticks,
        and pygame.joystick module."""
    if pygame.joystick.get_init():
        joysticks = [
            pygame.joystick.Joystick(x)
            for x in range(pygame.joystick.get_count()) 
            if pygame.joystick.Joystick(x).get_init()
        ]
        for joystick in joysticks:
            print ("quitting joystick {}".format(joystick))
            joystick.quit()
        pygame.joystick.quit()


def _get_joy_event_elems(event):
    """ gets the attributes from joystick event, be that 
        JOYBUTTONUP, JOYBUTTONDOWN or JOYAXISMOTION.
        returns a tuple with attributes or a tuple with one None,
        if no valid attributes found
        """
    axis = getattr(event, 'axis', None)
    value = getattr(event, 'value', None)
    if isinstance(value, numbers.Number):
        value = round(value)
    joy = getattr(event, 'joy', None)
    button = getattr(event, 'button', None)
    if axis is not None and value is not None and joy is not None:
        return joy, axis, value
    elif button is not None and joy is not None:
        return joy, button
    else:
        return (None, )


def map_joy_event_key_down(event):
    """ processes event if it is a pressed event
        returns the keyboard key from JOYSTICK_MAPPING"""
    elems = _get_joy_event_elems(event) #joy,axis,value or joy,button
    key = JOYSTICK_MAPPING.get((event.type, *elems))
    if key:
        _pressed.add(key)
    return key


def map_joy_event_key_up(event):
    """ processes event if it is a release event
        returns the keyboard key from JOYSTICK_MAPPING"""
    elems = _get_joy_event_elems(event) #joy,axis,value or joy,button
    partial_func = JOYSTICK_MAPPING.get((event.type, *elems))
    key = partial_func() if callable(partial_func) else partial_func
    if key:
        _pressed.remove(key)
    return key


def process_event(event):
    """ if event is a joystick event, build a keyboard event
        based on JOYSTICK mapping and post that event on
        pygame event loop.
        returns True if event was joystick event, False otherwise."""
    was_joystick_down = pgzero.controller.map_joy_event_key_down(event)
    was_joystick_up = pgzero.controller.map_joy_event_key_up(event)
    if was_joystick_down:
        pgzero.keyboard.keyboard._press(was_joystick_down)
        new_event = pygame.event.Event(pygame.KEYDOWN, key=was_joystick_down)
        pygame.event.post(new_event)
        return True
    elif was_joystick_up:
        pgzero.keyboard.keyboard._release(was_joystick_up)
        new_event = pygame.event.Event(pygame.KEYUP, key=was_joystick_up)
        pygame.event.post(new_event)
        return True
    return False