import collections
import numbers
import functools
import json

import pygame

import pgzero.keyboard
import pgzero.constants


_pressed = set()
# the joysticks that will be detected by pygame, during runtime
INITIALIZED_JOYS = {}
# the joysticks from joysticks.json (same mapping for all types of joysticks)
JOY_TYPES = {}
# the handlers for pygame joystick events
JOY_EVENTS_MAP = {}
# the joystick to keyboard bindings 
JOY_KEY_BINDINGS = {}


def _get_binding(joy, value):
    return JOY_KEY_BINDINGS.get(str(joy), {}).get("keybindings", {}).get(value)


def _joy_axis_release(joy, axis):
    # joy axis release events are the same for right&left or up&down
    # so look into _pressed set to see what was previously pressed.
    # but be wary:
    #  on joystick initialize the 'release' events for both axes are sent
    # TODO: we might want to not add those events to _pressed set
    dpads = ("dpadleft", "dpadright") if axis == 0 else ("dpadup", "dpaddown")
    option1 = _get_binding(joy, dpads[1])
    option2 = _get_binding(joy, dpads[0])
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


def get_joy_btn_name(joy, button):
    """ given a joy number and a button event number return a button name"""
    joy_name = INITIALIZED_JOYS[int(joy)] if len(INITIALIZED_JOYS) > int(joy) else 'snes'
    joy_type = JOY_TYPES.get(joy_name, {})
    buttons_match = [key for key in joy_type.keys() if joy_type[key] == button]
    return buttons_match[0] if buttons_match else None


def get_joy_button(joy, button):
    """ given a 'button_x' return the button value that we expect in event
        it uses the JOY_TYPES global"""
    joy_name = INITIALIZED_JOYS[int(joy)] if len(INITIALIZED_JOYS) > int(joy) else 'snes'
    return JOY_TYPES.get(joy_name, {}).get(button)


def _joy_buttons_mapping(joy):
    """ map all button bindings from constants to JOY_KEY_BINDINGS if found."""
    result = {}
    for button in pgzero.constants.joy_button:
        binding = _get_binding(joy, button.value)
        if binding:
            result[JoystickButtonEvent(
                type=pygame.JOYBUTTONDOWN,
                joy=joy,
                button=get_joy_button(joy, button.value)
            )] = binding
            result[JoystickButtonEvent(
                type=pygame.JOYBUTTONUP,
                joy=joy,
                button=get_joy_button(joy, button.value)
            )] = binding
    return result


def _joy_dpad_mapping(joy):
    """ map all axis/dpad bindings from constants to JOY_KEY_BINDINGS if found.
    """
    # TODO: there might be some way to differentiate between dpads and the joysticks
    result = {}
    dpads = {
        pgzero.constants.joy_axis.HORIZONTAL: ("dpadleft", "dpadright", ""),
        pgzero.constants.joy_axis.VERTICAL: ("dpadup", "dpaddown", ""),
    }
    for axis, dpad in dpads.items():
        for index, value in enumerate(pgzero.constants.joy_value):
            binding = _get_binding(joy, dpad[index])
            if binding:
                result[JoystickAxisEvent(
                    type=pygame.JOYAXISMOTION, joy=joy, axis=axis, value=value
                )] = binding
        released = pgzero.constants.joy_value.RELEASED
        result[JoystickAxisEvent(
            type=pygame.JOYAXISMOTION, joy=joy, axis=axis, value=released
        )] = functools.partial(_joy_axis_release, joy=joy, axis=axis)
    return result


def load_joy_key_bindings():
    JOY_KEY_BINDINGS.clear()
    with open('config/joy_key_bindings.json', 'r') as fp:
        JOY_KEY_BINDINGS.update(json.loads(fp.read()))


def build_joystick_mapping():
    """ build a dictionary with joystick events mapped to pygame keys.
        uses JOY_KEY_BINDINGS as basis."""
    JOY_EVENTS_MAP.clear()
    for joystick in JOY_KEY_BINDINGS.keys():
        result = _joy_buttons_mapping(int(joystick))
        result.update(_joy_dpad_mapping(int(joystick)))
        JOY_EVENTS_MAP.update(result)


def load_joysticks_types():
    JOY_TYPES.clear()
    with open('config/joysticks.json', 'r') as fp:
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
    for index, joystick in enumerate(joysticks):
        print ("initializing joystick {}".format(joystick.get_name()))
        INITIALIZED_JOYS[index] = joystick.get_name()
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