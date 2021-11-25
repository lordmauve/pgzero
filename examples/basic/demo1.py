WIDTH = 500
HEIGHT = 100
TITLE = "Fading Green!"

c = 0


def draw():
    screen.fill((0, c, 0))


def update(dt):
    global c, HEIGHT
    c = (c + 1) % 256
    if c == 255:
        HEIGHT += 10


def on_mouse_down(button, pos):
    print("Mouse button", button, "clicked at", pos)
