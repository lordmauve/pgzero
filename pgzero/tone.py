import re
from functools import lru_cache

import math
import pygame
import numpy
import pygame.sndarray

__all__ = ['create', 'play']

SAMPLE_RATE = 22050

NOTE_PATTERN = r'^([A-G])([b#]?)([0-8])$'

A4 = 440.0

NOTE_VALUE = dict(C=-9, D=-7, E=-5, F=-4, G=-2, A=0, B=2)

TWELTH_ROOT = math.pow(2, (1/12))


def sine_array_onecycle(hz):
    """Returns a single sin wave for a given frequency"""
    length = SAMPLE_RATE / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    return (numpy.sin(xvalues) * (2 ** 15)).astype(numpy.int16)


@lru_cache()
def create(hz, length):
    """Creates a tone of a certain length from a note or frequency in hertz"""
    if isinstance(hz, str):
        hz = note_to_hertz(hz)
    length *= float(SAMPLE_RATE)
    cycle = sine_array_onecycle(hz)
    num_cycles = length - length % len(cycle)
    tone = numpy.resize(cycle, num_cycles)
    stereo = numpy.array(list(zip(tone, tone)))
    return pygame.sndarray.make_sound(stereo)

class InvalidNote(Exception):
    pass

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
            '%s is not a valid note, notes are A-F, are either normal, flat (b) or sharp (#) and of octave 0-8' % note)
    note, accidental, octave = match.group(1, 2, 3)
    return note, accidental, int(octave)


def play(hz, length):
    """Plays a tone of a certain length from a note or frequency in hertz"""
    create(hz, length).play()
