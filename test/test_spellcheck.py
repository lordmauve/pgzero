from unittest import TestCase
from pgzero import spellcheck


class SuggestionTest(TestCase):
    HOOKS = spellcheck.HOOKS

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


class LoggingSpellCheckResult:
    def __init__(self):
        self.warnings = []
        self.errors = []

    def warn(self, msg, found, suggestion):
        self.warnings.append((found, suggestion))

    def error(self, msg, found, suggestion):
        self.errors.append((found, suggestion))

    def has_error(self, found, suggestion):
        return (found, suggestion) in self.errors

    def has_warning(self, found, suggestion):
        return (found, suggestion) in self.warnings

    def get_report(self):
        lines = []
        for type in ('warnings', 'errors'):
            msgs = getattr(self, type)
            if msgs:
                lines += [
                    'Got %s:' % type,
                ]
                lines += ['  %s -> %s' % m for m in msgs]
            else:
                lines += ['No %s emitted' % type]
        return '\n'.join(lines)


class SpellCheckerTest(TestCase):
    def setUp(self):
        self.result = LoggingSpellCheckResult()

    def assert_has_warning(self, found, suggestion):
        if self.result.has_warning(found, suggestion):
            return

        raise AssertionError(
            'Expected warning (%s -> %s)\n' % (found, suggestion) +
            self.result.get_report()
        )

    def assert_has_error(self, found, suggestion):
        if self.result.has_error(found, suggestion):
            return

        raise AssertionError(
            'Expected error (%s -> %s)\n' % (found, suggestion) +
            self.result.get_report()
        )

    def spellcheck(self, namespace):
        spellcheck.spellcheck(namespace, self.result)

    def test_misspelled_mousedown(self):
        self.spellcheck({
            'on_moose_down': lambda: None,
        })
        self.assert_has_warning('on_moose_down', 'on_mouse_down')

    def test_misspelled_width_uppercase(self):
        self.spellcheck({
            'WIDHT': 640,
        })
        self.assert_has_warning('WIDHT', 'WIDTH')

    def test_misspelled_width_lowercase(self):
        self.spellcheck({
            'widht': 640,
        })
        self.assert_has_warning('widht', 'WIDTH')

    def test_misspelled_width_mixed_lower_and_upper_case(self):
        self.spellcheck({
            'WIDht': 640,
        })
        self.assert_has_warning('WIDht', 'WIDTH')

    def test_misspelled_param(self):
        self.spellcheck({
            'on_mouse_down': lambda buton: None,
        })
        self.assert_has_error('buton', 'button')
