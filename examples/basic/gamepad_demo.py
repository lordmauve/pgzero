WIDTH = 300
HEIGHT = 400
TITLE = "gamepad demo"

# GAMEPAD_1_X_AXIS = 3
# GAMEPAD_1_Y_AXIS = 4

RED = (255,0,0)
GREEN = (0,255,0)

def draw():
    global pad1, pad2
    screen.fill((255, 255, 255))
    pad1.draw()
    pad2.draw()

def update():
    pass

def on_gamepad_1_pressed(button):
    print('GAMEPAD 1:', gamepad.name(button))
    pad1[gamepad.name(button)] = True

def on_gamepad_1_released(button):
    pad1[gamepad.name(button)] = False

def on_gamepad_2_pressed(button):
    print('GAMEPAD 2:', gamepad.name(button))
    pad2[gamepad.name(button)] = True

def on_gamepad_2_released(button):
    pad2[gamepad.name(button)] = False

class Gamepad:

    def __init__(self, number, offset):
        self.number = number
        self.offset = offset
        self.A = False
        self.B = False
        self.UP = False
        self.DOWN = False
        self.RIGHT = False
        self.LEFT = False

    def c(self,button):
        if button:
            return RED
        else:
            return GREEN

    def draw(self):
        oy = self.offset
        screen.draw.filled_rect(Rect(40,30+oy,220,150), (200, 200, 200))
        screen.draw.filled_circle((100,70+oy), 20, self.c(self.UP))
        screen.draw.filled_circle((130,100+oy), 20, self.c(self.RIGHT))
        screen.draw.filled_circle((100,130+oy), 20, self.c(self.DOWN))
        screen.draw.filled_circle((70,100+oy), 20, self.c(self.LEFT))

        screen.draw.filled_circle((180,130+oy), 20, self.c(self.B))
        screen.draw.filled_circle((230,130+oy), 20, self.c(self.A))

        screen.draw.text('gamepad {}'.format(self.number), (170, 35+oy))

    def __setitem__(self, key, value):
        if key == 'A':
            self.A = value
        elif key == 'B':
            self.B = value
        elif key == 'UP':
            self.UP = value
        elif key == 'RIGHT':
            self.RIGHT = value
        elif key == 'DOWN':
            self.DOWN = value
        elif key == 'LEFT':
            self.LEFT = value

pad1 = Gamepad(1, 0)
pad2 = Gamepad(2, 180)
