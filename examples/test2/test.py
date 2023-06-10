from functools import partial

TILE_SIZE = 24

TILES_W = 20
TILES_H = 15

WIDTH = TILE_SIZE * TILES_W
HEIGHT = TILE_SIZE * TILES_H


def screen_rect(tile_pos):
    """Get the screen rectangle for the given tile coordinate."""
    x, y = tile_pos
    return Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)

alien = Actor('alien', (50, 50))

def set_alien_normal(alien, color):
    alien.image = 'alien_'+color

def update():
    if keyboard.left:
        alien.x -= 1
    elif keyboard.right:
        alien.x += 1


def test1():
    print("test1")
def test2(i,j):
    print(str(i)+str(j))

clock.schedule_unique(partial(test2,2,3), 1.0)
clock.schedule_unique(test1, 2.0)
clock.schedule_unique(partial(set_alien_normal, alien, 'blue'), 1.0)
clock.schedule_unique(partial(set_alien_normal, alien, 'gray'), 5.0)
clock.schedule_unique(partial(set_alien_normal,alien,'purple'), 10.0)
clock.schedule_unique(partial(set_alien_normal,alien,'green'), 15.0)



def draw():
    screen.clear()
    alien.draw()

