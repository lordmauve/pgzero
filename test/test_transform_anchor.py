from math import sin, cos, radians
from unittest import TestCase
from pgzero.actor import transform_anchor

root2 = 2 ** 0.5


def assertVecEqual(a, b, decimal_places=7):
    for t in (a, b):
        if not isinstance(t, tuple):
            raise AssertionError('%r is not a tuple' % t)
        if len(t) != 2:
            raise AssertionError('Expected 2-tuple, not %r' % t)

    ax, ay = a
    bx, by = b
    epsilon = 10 ** -decimal_places
    if abs(ax - bx) > epsilon or abs(ay - by) > epsilon:
        raise AssertionError('%r != %r (to %d decimal places)' % (
            a, b, decimal_places
        ))


class TransformAnchorTest(TestCase):
    def test_identity(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 0),
            (5, 5)
        )

    def test_45deg(self):
        assertVecEqual(
            transform_anchor(5, 5, 10, 10, 45),
            (5 * root2, 5 * root2)
        )

    def test_45deg_offset(self):
        assertVecEqual(
            transform_anchor(0, 0.5, 1, 1, 45),
            (0.25 * root2, 0.75 * root2)
        )
