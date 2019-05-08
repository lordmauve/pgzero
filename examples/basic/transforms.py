WIDTH = 1024
HEIGHT = 800

ship = Actor('ship')
ship.pos = 200, 200


def draw():
    screen.fill((255, 255, 255))
    ship.draw()

def on_mouse_move(pos):
    ship.pos = pos

def on_key_down(key):
    if key == keys.LEFT:
        ship.angle -= 10
    elif key == keys.RIGHT:
        ship.angle += 10
    elif key == keys.UP:
        x, y = ship.dimensions
        ship.dimensions = x + 5, y + 5
    elif key == keys.DOWN:
        x, y = ship.dimensions
        # pygamezero will raise an exception if we set negative dimensions.
        if x > 5 and y > 5:
            ship.dimensions = x - 5, y - 5
    elif key == keys.SPACE:
        ship.flip_x()
    elif key == keys.TAB:
        ship.flip_y()
