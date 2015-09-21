from unittest import TestCase

import numpy

from pgzero.tone import sine_array_onecycle


class ToneTest(TestCase):
    def test_sine_array(self):
        numpy.allclose(
            sine_array_onecycle(2205),
            numpy.array(
                [0, 19260, 31164, 31164, 19260, 0, -19260, -31164, -31164, -19260],
                dtype=numpy.int16
            )
        )
