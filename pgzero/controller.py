import collections
import pygame
import pgzero.keyboard

_pressed = set()
GAMEPADS = {
    0: {
        "id": 0,
        "keybindings": {
            "dpadleft": pygame.K_a,
            "dpadright": pygame.K_d,

        }
    }
}

def initialize_joysticks():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print ("initializing joystick {}".format(joystick))
        joystick.init()

JoystickAxisEvent = collections.namedtuple('JoystickAxisEvent', 'type,axis,value')
JOYSTICK_MAPPING = {
    JoystickAxisEvent(type=pygame.JOYAXISMOTION, axis=0, value=-1): pygame.K_LEFT,
    JoystickAxisEvent(type=pygame.JOYAXISMOTION, axis=0, value=1): pygame.K_RIGHT,
    JoystickAxisEvent(type=pygame.JOYAXISMOTION, axis=1, value=-1): pygame.K_UP,
    JoystickAxisEvent(type=pygame.JOYAXISMOTION, axis=1, value=1): pygame.K_DOWN,
}

def map_joy_event_key_down(event):
    axis = getattr(event, 'axis', None)
    value = getattr(event, 'value', None) and round(getattr(event, 'value'))
    key = JOYSTICK_MAPPING.get((event.type, axis, value))
    if key:
        _pressed.add(key)
    return key


def map_joy_event_key_up(event):
    if event.type == pygame.JOYAXISMOTION:
        axis = event.axis
        value = round(event.value)
        if axis == 0 and value == 0:
            if pygame.K_LEFT in _pressed:
                print("key A release")
                _pressed.remove(pygame.K_LEFT)
                return pygame.K_LEFT
            elif pygame.K_RIGHT in _pressed:
                print("key D release")
                _pressed.remove(pygame.K_RIGHT)
                return pygame.K_RIGHT
        if axis == 1 and value == 0:
            if pygame.K_UP in _pressed:
                print("key W release")
                _pressed.remove(pygame.K_UP)
                return pygame.K_UP
            elif pygame.K_DOWN in _pressed:
                print("key S release")
                _pressed.remove(pygame.K_DOWN)
                return pygame.K_DOWN
    if event.type == pygame.JOYBUTTONUP:
        if event.button == 3:
            print("key SPACE")
            return 32
    return 0
