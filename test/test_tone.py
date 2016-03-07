from unittest import TestCase

import numpy

from pgzero.tone import sine_array_onecycle, note_value
from tone import note_to_hertz


class ToneTest(TestCase):
    def test_sine_array(self):
        numpy.allclose(
            sine_array_onecycle(2205),
            numpy.array(
                [0, 19260, 31164, 31164, 19260, 0, -19260, -31164, -31164, -19260],
                dtype=numpy.int16
            )
        )

    def test_note_value(self):
        self.assertEqual(note_value('A4'), 0)
        self.assertEqual(note_value('C4'), -9)
        self.assertEqual(note_value('C0'), -57)
        self.assertEqual(note_value('B8'), 50)
        self.assertEqual(note_value('A#4'), 1)
        self.assertEqual(note_value('Bb4'), 1)


    def test_note_to_hertz(self):
        self.assertAlmostEqual(note_to_hertz('A4'), 440, 2)
        self.assertAlmostEqual(note_to_hertz('C4'), 261.63, 2)
        self.assertAlmostEqual(note_to_hertz('C0'), 16.35, 2)
        self.assertAlmostEqual(note_to_hertz('B8'), 7902.13, 2)
        self.assertAlmostEqual(note_to_hertz('A#4'), 466.16, 2)
        self.assertAlmostEqual(note_to_hertz('Bb4'), 466.16, 2)

