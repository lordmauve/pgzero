WIDTH = 500
HEIGHT = 100
TITLE = "gamepad"

# GAMEPAD_1_X_AXIS = 0
# GAMEPAD_1_Y_AXIS = 1
# GAMEPAD_2_X_AXIS = 3
# GAMEPAD_2_Y_AXIS = 4

def draw():
    screen.fill((0, 0, 0))

def update():
    # You can use an attribute to get the button that was pressed
    if gamepad_1.UP:
        print('UP ON ONE')

    # It can be lower or uppercase
    if gamepad_1.a:
        print('A ON ONE')

    # You can also index with the button constant
    if gamepad_1[gamepad.DOWN]:
        print('DOWN ON ONE')

def on_gamepad_1_pressed(button):
    print('GAMEPAD 1 PRESSED:', gamepad.name(button))

def on_gamepad_1_released(button):
    print('GAMEPAD 1 RELEASED:', gamepad.name(button))

def on_gamepad_2_pressed(button):
    print('GAMEPAD 2 PRESSED:', gamepad.name(button))

def on_gamepad_2_released(button):
    print('GAMEPAD 2 RELEASED:', gamepad.name(button))
