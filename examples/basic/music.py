playing = None

music.set_volume(0.5)

tracks = [
    'handel_mp3',
    'handel_ogg',
]


def draw():
    if not playing:
        msg = 'Click to start'
    else:
        msg = 'Playing ' + playing
    screen.clear()
    screen.draw.text(
        msg,
        fontsize=70,
        center=(400, 300)
    )


def on_mouse_down():
    global playing

    t = tracks.pop(0)
    music.play(t)
    playing = t
    tracks.append(t)


def on_music_end():
    global playing
    playing = None
