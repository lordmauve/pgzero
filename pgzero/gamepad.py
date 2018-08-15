import pygame
from warnings import warn

class Gamepad:
    _pressed = set()

    def __init__(self, joystick, key_bindings):
        self.joystick_number = joystick
        self.key_bindings = key_bindings
        self.reverse_key_bindings = {}
        self.handler = None
        self.press_handler = None
        self.release_handler = None
        for name, key in self.key_bindings.items():
            self.reverse_key_bindings[key] = name
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(joystick-1)
            self.joystick.init()
            print(self.joystick.get_name())
        except pygame.error:
            pass

    def prepare(self, game):
        handler = getattr(game.mod, 'on_gamepad_{}'.format(self.joystick_number), None)
        if(callable(handler)):
            self.handler = handler
        press_handler = getattr(game.mod, 'on_gamepad_{}_pressed'.format(self.joystick_number), None)
        if(callable(press_handler)):
            self.press_handler = press_handler
        release_handler = getattr(game.mod, 'on_gamepad_{}_released'.format(self.joystick_number), None)
        if(callable(release_handler)):
            self.release_handler = release_handler
        self.x_axis = getattr(game.mod, 'GAMEPAD_{}_X_AXIS'.format(self.joystick_number), 0)
        self.y_axis = getattr(game.mod, 'GAMEPAD_{}_Y_AXIS'.format(self.joystick_number), 1)

    def press(self, button):
        self._pressed.add(button)
        self.dispatch(pygame.KEYDOWN, button)

    def release(self, button):
        self._pressed.discard(button)
        self.dispatch(pygame.KEYUP, button)

    def dispatch(self, type, button):
        if self.handler:
            self.handler(Event(type, button))
        if type == pygame.KEYDOWN and self.press_handler:
            self.press_handler(button)
        if type == pygame.KEYUP and self.release_handler:
            self.release_handler(button)

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.reverse_key_bindings.keys():
                name = self.reverse_key_bindings[event.key]
                button = buttons[name]
                self.press(button)
        if event.type == pygame.KEYUP:
            if event.key in self.reverse_key_bindings.keys():
                name = self.reverse_key_bindings[event.key]
                button = buttons[name]
                self.release(button)
        if event.type == pygame.JOYBUTTONDOWN and event.joy == self.joystick_number-1:
            if event.button == 1:
                self.press(A)
            if event.button == 2:
                self.press(B)
        if event.type == pygame.JOYBUTTONUP and event.joy == self.joystick_number-1:
            if event.button == 1:
                self.release(A)
            if event.button == 2:
                self.release(B)
        if event.type == pygame.JOYAXISMOTION:
            if event.joy == self.joystick_number-1:
                value = int(round(event.value))
                if event.axis == self.x_axis:
                    if value == -1:
                        self.press(LEFT)
                    if value == 1:
                        self.press(RIGHT)
                    if value == 0:
                        if LEFT in self._pressed:
                            self.release(LEFT)
                        if RIGHT in self._pressed:
                            self.release(RIGHT)
                if event.axis == self.y_axis:
                    if value == -1:
                        self.press(UP)
                    if value == 1:
                        self.press(DOWN)
                    if value == 0:
                        if UP in self._pressed:
                            self.release(UP)
                        if DOWN in self._pressed:
                            self.release(DOWN)

    def __getattr__(self, button):
        return buttons[button]

    def __getitem__(self, button):
        return button in self._pressed

class Buttons:

    def __init__(self):
        self.button_names = {}
        for name, key in buttons.items():
            self.button_names[key] = name

    def __getattr__(self, button):
        return buttons[button]

    def name(self, button):
        return self.button_names[button]

class Event:

    def __init__(self, type, button):
        self.type = type
        self.button = button

keybindings_1 = {
    'UP': pygame.K_w,
    'RIGHT': pygame.K_d,
    'DOWN': pygame.K_s,
    'LEFT': pygame.K_a,
    'A': pygame.K_SPACE,
    'B': None
}

keybindings_2 = {
    'UP': pygame.K_i,
    'RIGHT': pygame.K_l,
    'DOWN': pygame.K_k,
    'LEFT': pygame.K_j,
    'A': pygame.K_m,
    'B': None
}

UP = (0)
RIGHT = (1)
DOWN = (2)
LEFT = (3)
A = (4)
B = (5)

buttons = {
    'UP': UP,
    'RIGHT': RIGHT,
    'DOWN': DOWN,
    'LEFT': LEFT,
    'A': A,
    'B': B
}

gamepad_1 = Gamepad(1, keybindings_1)
gamepad_2 = Gamepad(2, keybindings_2)
gamepad = Buttons()
gamepad.PRESSED = pygame.KEYDOWN
gamepad.RELEASED = pygame.KEYUP

