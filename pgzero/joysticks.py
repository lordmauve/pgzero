import collections
import numbers
import functools
import json

import pygame

import pgzero.keyboard

_pressed = set()
# the joysticks that will be detected by pygame, during runtime
INITIALIZED_JOYS = []
# the joysticks from joysticks.json (same mapping for all types of joysticks)
JOY_TYPES = {}
# the handlers for pygame joystick events
JOY_EVENTS_MAP = {}
# the joystick to keyboard bindings 
JOY_KEY_BINDINGS = {}


def _joy_axis_release(joy, axis):
    # joy axis release events are the same for right&left or up&down
    # so look into _pressed set to see what was previously pressed.
    # but be wary:
    #  on joystick initialize the 'release' events for both axes are sent
    # TODO: we might want to not add those events to _pressed set
    dpads = ("dpadleft", "dpadright") if axis == 0 else ("dpadup", "dpaddown")
    option1 = JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get(dpads[1])
    option2 = JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get(dpads[0])
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


def get_joy_button(joy, button):
    joy_name = INITIALIZED_JOYS[int(joy)] if len(INITIALIZED_JOYS) > int(joy) else 'snes'
    return JOY_TYPES.get(joy_name, {}).get(button)

def one_joystick_mapping(joy):
    """ map joystick events from a single joystick to JOYSTICKS keybindings."""
    return {
        # pressed events
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=0, value=-1
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("dpadleft"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=0, value=1
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("dpadright"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=1, value=-1
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("dpadup"),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=1, value=1
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("dpaddown"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joy, button=get_joy_button(joy, 'button_x')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_x"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joy, button=get_joy_button(joy, 'button_a')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_a"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joy, button=get_joy_button(joy, 'button_b')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_b"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONDOWN, joy=joy, button=get_joy_button(joy, 'button_y')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_y"),
        # release events
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=0, value=0
        ): functools.partial(_joy_axis_release, joy=joy, axis=0),
        JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=1, value=0
        ): functools.partial(_joy_axis_release, joy=joy, axis=1),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joy, button=get_joy_button(joy, 'button_x')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_x"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joy, button=get_joy_button(joy, 'button_a')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_a"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joy, button=get_joy_button(joy, 'button_b')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_b"),
        JoystickButtonEvent(
            type=pygame.JOYBUTTONUP, joy=joy, button=get_joy_button(joy, 'button_y')
        ): JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get("button_y"),
    }


def load_joy_key_bindings():
    with open('joy_key_bindings.json', 'r') as fp:
        JOY_KEY_BINDINGS.update(json.loads(fp.read()))


def build_joystick_mapping():
    """ build a dictionary with josytick events mapped to pygame keys.
        uses INITIALIZED_JOYS as basis."""
    for joystick in JOY_KEY_BINDINGS.keys():
        JOY_EVENTS_MAP.update(one_joystick_mapping(int(joystick)))


def load_joysticks_types():
    with open('joysticks.json', 'r') as fp:
        JOY_TYPES.update(json.loads(fp.read()))


def initialize_joysticks():
    """ initialize pygame.joystick module,
        and call init on available joysticks."""
    # load internal mappings
    load_joysticks_types()
    load_joy_key_bindings()
    build_joystick_mapping()
    # initialize pygame joysticks
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print ("initializing joystick {}".format(joystick.get_name()))
        INITIALIZED_JOYS.append(joystick.get_name())
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
            print ("quitting joystick {}".format(joystick.get_name()))
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
        returns the keyboard key from JOY_EVENTS_MAP"""
    elems = _get_joy_event_elems(event) #joy,axis,value or joy,button
    key = JOY_EVENTS_MAP.get((event.type, *elems))
    if key:
        _pressed.add(key)
    return key


def map_joy_event_key_up(event):
    """ processes event if it is a release event
        returns the keyboard key from JOY_EVENTS_MAP"""
    elems = _get_joy_event_elems(event) #joy,axis,value or joy,button
    partial_func = JOY_EVENTS_MAP.get((event.type, *elems))
    key = partial_func() if callable(partial_func) else partial_func
    if key:
        _pressed.remove(key)
    return key


def process_event(event):
    """ if event is a joystick event, build a keyboard event
        based on JOY_KEY_BINDINGS mapping and post that event on
        pygame event loop.
        returns True if event was joystick event, False otherwise."""
    was_joystick_down = map_joy_event_key_down(event)
    was_joystick_up = map_joy_event_key_up(event)
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