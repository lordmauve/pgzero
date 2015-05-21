import os.path
from pygame.mixer import Sound

SOUND_PATH = 'sound'


def load_sound(filename):
    path = os.path.join(SOUND_PATH, filename + '.ogg')
    return Sound(path)


music_name = None
music_playing = None


def play_music(name):
    global music_playing, music_name
    if music_name == name:
        return

    if music_playing:
        music_playing.stop()

    music_name = name
    music_playing = load_sound(name)
    music_playing.set_volume(0.4)
    music_playing.play(-1)
