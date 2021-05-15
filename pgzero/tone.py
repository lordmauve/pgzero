"""Tone generator for Pygame Zero.

This tone generator is a wrapper for pyfxr, a custom Cython library for sound
generation. Tones are kept in a LRU cache which in typical applications
will reduce the number of times they need to be regenerated.

To minimise the extent that pauses affect gameplay, the ``play()`` function
offloads tone generation to a separate thread. Because tones are generated
with numpy operations this should allow at least part of this work to happen
on another CPU core, if present.

"""
from functools import lru_cache
from collections import namedtuple
from threading import Thread, Lock
from queue import Queue
from enum import Enum

import pygame
import pyfxr


__all__ = (
    'play',
    'create',
)


# Longest note to allow
MAX_DURATION = 4


class Waveform(Enum):
    SIN = pyfxr.Wavetable.sine()
    SQUARE = pyfxr.Wavetable.square()
    SAW = pyfxr.Wavetable.saw()
    TRIANGLE = pyfxr.Wavetable.triangle()


ToneParams = namedtuple('ToneParams', 'hz duration waveform volume')


# lru_cache isn't threadsafe until Python 3.7, so protect it ourselves
# https://bugs.python.org/issue28969
cache_lock = Lock()
note_queue = Queue()
player_thread = None


def _play_thread():
    """Play any notes requested by the game thread.

    Multithreading is useful because numpy releases the GIL while performing
    many C operations.

    """
    while True:
        params = note_queue.get()
        with cache_lock:
            note = _create(params)
        note.play()


def create(*args, **kwargs):
    """Create a tone of a given duration at the given pitch.

    Return a Sound which can be played later.

    """
    params = _convert_args(*args, **kwargs)
    with cache_lock:
        return _create(params)


@lru_cache()
def _create(params):
    """Actually create a tone."""
    # Construct a mono tone of the right length
    tone = pyfxr.tone(
        pitch=params.hz,
        sustain=max(0, params.duration - 0.2),
        wavetable=params.waveform.value,
    )

    # NB. pygame assumes that the sound format of any buffer object matches
    # that of the current mixer settings. We use mixer.pre_init(22050, -16, 2)
    # which means that it is expecting 22kHz audio stereo, but we're feeding it
    # 44kHz mono - but, perhaps surprisingly, that works Ok. The extra samples
    # get interpreted as the second channel.
    #
    # If we change the mixer to 44kHz we'd need to convert to stereo here by
    # doubling samples.
    #
    # Really this is a mess and Pygame should support converting the format
    # of buffers (as it does for .wav files).
    snd = pygame.mixer.Sound(buffer=tone)
    snd.set_volume(params.volume)
    return snd


def _convert_args(pitch, duration, *, waveform=Waveform.SIN, volume=0.8):
    """Convert the given arguments to _create parameters."""
    if duration > MAX_DURATION:
        raise ValueError(
            'Note duration %ss is too long: notes may be at most %ss long' %
            (duration, MAX_DURATION)
        )
    if not duration:
        raise ValueError("Note has zero duration")
    return ToneParams(pitch, duration, Waveform(waveform), volume)


def play(*args, **kwargs):
    """Plays a tone of a certain length from a note or frequency in hertz.

    Tones have a maximum duration of 4 seconds. This limitation is imposed to
    avoid accidentally creating sounds that take too long to generate and
    require a lot of memory.

    To work around this, create the sounds you want to use up-front with
    create() and hold onto them, perhaps in an array.

    """
    global player_thread
    params = _convert_args(*args, **kwargs)
    if not player_thread or not player_thread.is_alive():
        pygame.mixer.init()
        player_thread = Thread(target=_play_thread, daemon=True)
        player_thread.start()
    note_queue.put(params)
