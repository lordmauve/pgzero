from unittest import TestCase
from pgzero.actor import BoundingBox

root2 = 2 ** 0.5


def rotate_anchor(anchor, w, h, angle):
    box = BoundingBox(w, h, anchor)
    box.set_angle(angle)
    return box.anchor


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


class RotateTest(TestCase):
    def test_identity(self):
        assertVecEqual(
            rotate_anchor((5, 5), 10, 10, 0),
            (5, 5)
        )

    def test_45deg(self):
        assertVecEqual(
            rotate_anchor((5, 5), 10, 10, 45),
            (5 * root2, 5 * root2)
        )

    def test_45deg_offset(self):
        assertVecEqual(
            rotate_anchor((0, 0.5), 1, 1, 45),
            (0.25 * root2, 0.75 * root2)
        )


class ScaleTest(TestCase):
    def setUp(self):
        self._box = BoundingBox(10, 10, (1, 2))

    def test_identity(self):
        self._box.set_dimensions((10, 10))
        assertVecEqual(self._box.anchor, (1, 2))

    def test_shrink(self):
        self._box.set_dimensions((4, 5))
        assertVecEqual(self._box.anchor, (0.4, 1))


class FlipTest(TestCase):
    def setUp(self):
        self._box = BoundingBox(10, 10, (1, 2))

    def test_identity(self):
        self._box.set_flip(False, False)
        assertVecEqual(self._box.anchor, (1, 2))

    def test_flipx(self):
        self._box.set_flip(True, False)
        assertVecEqual(self._box.anchor, (9, 2))

    def test_flipy(self):
        self._box.set_flip(False, True)
        assertVecEqual(self._box.anchor, (1, 8))
