WIDTH = 500
HEIGHT = 100
TITLE = "gamepad"
GAMEPAD_1_X_AXIS = 3
GAMEPAD_1_Y_AXIS = 4

def draw():
    screen.fill((0, 0, 0))

def update():
    pass

def on_gamepad_1_pressed(button):
    print('GAMEPAD 1:', gamepad.name(button))

def on_gamepad_2_pressed(button):
    print('GAMEPAD 2:', gamepad.name(button))

