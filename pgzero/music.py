from pygame.mixer import music as _music
from .loaders import ResourceLoader
from . import constants


__all__ = [
    'rewind', 'stop', 'fadeout', 'set_volume', 'get_volume', 'get_pos',
    'set_pos', 'play', 'queue', 'pause', 'unpause',
]

_music.set_endevent(constants.MUSIC_END)


class _MusicLoader(ResourceLoader):
    """Pygame's music API acts as a singleton with one 'current' track.

    No objects are returned that represent different tracks, so this loader
    can't return anything useful. But it can perform all the path name
    validations and return the validated path, so that's what we do.

    This loader should not be exposed to the user.

    """
    EXTNS = ['mp3', 'ogg', 'oga']
    TYPE = 'music'

    def _load(self, path):
        return path

_loader = _MusicLoader('music')


# State of whether we are paused or not
_paused = False


def _play(name, loop):
    global _paused
    path = _loader.load(name)
    _music.load(path)
    _music.play(loop)
    _paused = False


def play(name):
    """Play a music file from the music/ directory.

    The music will loop when it finishes playing.

    """
    _play(name, -1)


def play_once(name):
    """Play a music file from the music/ directory."""
    _play(name, 0)


def queue(name):
    """Queue a music file to follow the current track.

    This will load a music file and queue it. A queued music file will begin as
    soon as the current music naturally ends. If the current music is ever
    stopped or changed, the queued song will be lost.

    """
    path = _loader.load(name)
    _music.queue(path)


def is_playing(name):
    """Return True if the music is playing and not paused."""
    return _music.get_busy() and not _paused


def pause():
    """Temporarily stop playback of the music stream.

    Call `unpause()` to resume.

    """
    global _paused
    _music.pause()
    _paused = True


def unpause():
    """Resume playback of the music stream after it has been paused."""
    global _paused
    _music.unpause()
    _paused = False


def fadeout(seconds):
    """Fade out and eventually stop the music playback.

    :param seconds: The duration in seconds over which the sound will be faded
                    out. For example, to fade out over half a second, call
                    ``music.fadeout(0.5)``.

    """
    _music.fadeout(int(seconds * 1000))


rewind = _music.rewind
stop = _music.stop
get_volume = _music.get_volume
set_volume = _music.set_volume
get_pos = _music.get_pos
set_pos = _music.set_pos
