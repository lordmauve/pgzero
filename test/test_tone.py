import re
from unittest import TestCase

import numpy

from pgzero.tone import (
    sine_array_onecycle, note_value,
    note_to_hertz, validate_note, InvalidNote
)

TEST_NOTES = {
    'A4': dict(val = 0, hertz = 440, parts = ('A', '', 4)),
    'C4': dict(val = -9, hertz = 261.63, parts = ('C', '', 4)),
    'C0': dict(val = -57, hertz = 16.35, parts = ('C', '', 0)),
    'B8': dict(val = 50, hertz = 7902.13, parts = ('B', '', 8)),
    'A#4': dict(val = 1, hertz = 466.16, parts = ('A', '#', 4)),
    'Ab4': dict(val = -1, hertz = 415.30, parts = ('A', 'b', 4)),
    'Bb4': dict(val = 1, hertz = 466.16, parts = ('B', 'b', 4)),
}

class ToneTest(TestCase):
    def test_sine_array(self):
        numpy.allclose(
            sine_array_onecycle(2205),
            numpy.array(
                [0, 19260, 31164, 31164, 19260, 0, -19260, -31164, -31164, -19260],
                dtype=numpy.int16
            )
        )

    def test_validate_note(self):
        for note, val in TEST_NOTES.items():
            self.assertEqual(validate_note(note), val['parts'])

        for note in ['A9', 'H4', '4A', 'a4', 'Az4']:
            with self.assertRaisesRegex(InvalidNote, re.escape('%s is not a valid note. notes are A-F, are either normal, flat (b) or sharp (#) and of octave 0-8' % note)):
                validate_note(note)

    def test_note_value(self):
        for note, val in TEST_NOTES.items():
            self.assertEqual(note_value(*val['parts']), val['val'])


    def test_note_to_hertz(self):
        for note, val in TEST_NOTES.items():
            self.assertAlmostEqual(note_to_hertz(note), val['hertz'], 2)

