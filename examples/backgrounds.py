background = 'water'


def draw():
    if background == 'water':
        screen.draw_water_background()
    elif background == 'space':
        screen.draw_space_background()


def on_mouse_down():
    global background
    if background == 'space':
        background = 'water'
    else:
        background = 'space'
