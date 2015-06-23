from unittest import TestCase
from pgzero import spellcheck


class SpellCheckerTest(TestCase):
    HOOKS = [  # This is the real list of hooks
        'draw',
        'update',
        'on_mouse_down',
        'on_mouse_up',
        'on_mouse_move',
        'on_key_down',
        'on_key_up',
    ]

    def assert_suggestions(self, w, candidates, expected):
        suggestions = spellcheck.suggest(w, candidates)
        self.assertEqual(suggestions, expected)

    def assert_best_suggestion(self, w, expected):
        suggestions = spellcheck.suggest(w, self.HOOKS)
        self.assertEqual(suggestions[0], expected)

    def test_distance_zero(self):
        self.assertEqual(
            spellcheck.distance('on_mouse_down', 'on_mouse_down'),
            0
        )

    def test_misspelled(self):
        """With only one suggestion, return it."""
        self.assert_suggestions('drow', ['draw'], ['draw'])

    def test_not_misspelled(self):
        """With only completely different words, there are no candidates."""
        self.assert_suggestions('fire_laser', ['draw', 'update'], [])

    def test_misspelled_on_mouse_down(self):
        self.assert_best_suggestion('onmousedown', 'on_mouse_down')

    def test_misspelled_on_mouse_down2(self):
        self.assert_best_suggestion('onMouseDown', 'on_mouse_down')

    def test_misspelled_on_mouse_down3(self):
        self.assert_best_suggestion('on_muose_Down', 'on_mouse_down')

    def test_misspelled_on_mouse_down4(self):
        self.assert_best_suggestion('on_mouse_don', 'on_mouse_down')
