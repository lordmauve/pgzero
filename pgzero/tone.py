"""Tone generator for Pygame Zero.

This tone generator uses numpy to generate sounds on demand at a given duration
and frequency. These are kept in a LRU cache which in typical applications
will reduce the number of times they need to be regenerated.

Rather than generating plain sine waves, tones are shaped by a basic and
hard-coded `Attack Decay Sustain Release (ADSR) envelope`__, which gives them a
slightly more sonorous timbre:

.. __: https://en.wikipedia.org/wiki/Synthesizer#ADSR_envelope

The approach we use here, generating sound samples in memory, is memory hungry
and can introduce pauses when tones are generated. Currently tones generate in
under 1ms on a 2.4GHz i7.

To minimise the extent that pauses affect gameplay, the ``play()`` function
offloads tone generation to a separate thread. Because tones are generated
with numpy operations this should allow at least part of this work to happen
on another CPU core, if present.

"""

from timeit import default_timer
import re
from functools import lru_cache

import math
import pygame
try:
    import numpy as np
except ImportError:
    np = None
import pygame.sndarray
from threading import Thread, Lock
from queue import Queue

__all__ = (
    'play',
    'create',
)

SAMPLE_RATE = 22050

NOTE_PATTERN = r'^([A-G])([b#]?)([0-8])$'

A4 = 440.0

NOTE_VALUE = dict(C=-9, D=-7, E=-5, F=-4, G=-2, A=0, B=2)

TWELTH_ROOT = math.pow(2, (1 / 12))

# Number of samples to decay for
DECAY = 2000

# Longest note to allow
MAX_DURATION = 4


# lru_cache isn't threadsafe until Python 3.7, so protect it ourselves
# https://bugs.python.org/issue28969
cache_lock = Lock()
note_queue = Queue()


def _play_thread():
    """Play any notes requested by the game thread.

    Multithreading is useful because numpy releases the GIL while performing
    many C operations.

    """
    while True:
        args = note_queue.get()
        with cache_lock:
            note = _create(*args)
        note.play()

player_thread = Thread(target=_play_thread)
player_thread.setDaemon(True)


def sine_array_onecycle(hz):
    """Returns a single sin wave for a given frequency."""
    length = SAMPLE_RATE / hz
    omega = np.pi * 2 / length
    xvalues = np.arange(int(length)) * omega
    return (np.sin(xvalues) * (2 ** 15)).astype(np.int16)


def create(pitch, duration):
    """Create a tone of a given duration at the given pitch.

    Return a Sound which can be played later.

    """
    with cache_lock:
        return _create(*_convert_args(pitch, duration))


@lru_cache()
def _create(hz, samples):
    """Actually create a tone."""
    end = samples + DECAY

    # Construct a mono tone of the right length
    cycle = sine_array_onecycle(hz)
    tone = np.resize(cycle, end)

    # Multiply it with an ADSR envelope
    # See https://en.wikipedia.org/wiki/Synthesizer#ADSR_envelope
    if samples < 1000:
        volumes = [0, 1, 0.9, 0]
        volume_times = [0, samples * 0.1, samples, end]
    else:
        volumes = [0, 1.0, 0.7, 0.7, 0]
        volume_times = [0, 350, 1000, samples, end]
    adsr = np.interp(np.arange(end), volume_times, volumes)
    np.multiply(tone, adsr, out=tone, casting='unsafe')

    stereo = np.repeat(np.expand_dims(tone, axis=1), 2, axis=1)
    return pygame.sndarray.make_sound(stereo)


class InvalidNote(Exception):
    """The parameters passed were invalid."""


@lru_cache()
def note_to_hertz(note):
    note, accidental, octave = validate_note(note)
    value = note_value(note, accidental, octave)
    return A4 * math.pow(TWELTH_ROOT, value)


def note_value(note, accidental, octave):
    value = NOTE_VALUE[note]
    if accidental:
        value += 1 if accidental == '#' else -1
    return (4 - octave) * -12 + value


def validate_note(note):
    match = re.match(NOTE_PATTERN, note)
    if match is None:
        raise InvalidNote(
            '%s is not a valid note. '
            'notes are A-F, are either normal, flat (b) or sharp (#) '
            'and of octave 0-8' % note
        )
    note, accidental, octave = match.group(1, 2, 3)
    return note, accidental, int(octave)


def _convert_args(hz, duration):
    """Convert the given arguments to _create parameters."""
    if isinstance(hz, str):
        hz = note_to_hertz(hz)
    samples = int(duration * SAMPLE_RATE)
    if not samples:
        raise InvalidNote("Note has zero duration")
    return hz, samples


def play(pitch, duration):
    """Plays a tone of a certain length from a note or frequency in hertz.

    Tones have a maximum duration of 4 seconds. This limitation is imposed to
    avoid accidentally creating sounds that take too long to generate and
    require a lot of memory.

    To work around this, create the sounds you want to use up-front with
    create() and hold onto them, perhaps in an array.

    """
    if duration > MAX_DURATION:
        raise InvalidNote(
            'Note duration %ss is too long: notes may be at most %ss long' %
            (duration, MAX_DURATION)
        )
    args = _convert_args(pitch, duration)
    if not player_thread.is_alive():
        player_thread.start()
    note_queue.put(args)


if np is None:
    def play(hz, length):
        raise RuntimeError(
            'Tone generation depends on Numpy, which is not available'
        )
