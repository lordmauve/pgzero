import re
from unittest import TestCase

from pgzero.tone import _convert_args


TEST_NOTES = {
    'A4': dict(val=0, hertz=440, parts=('A', '', 4)),
    'C4': dict(val=-9, hertz=261.63, parts=('C', '', 4)),
    'C0': dict(val=-57, hertz=16.35, parts=('C', '', 0)),
    'B8': dict(val=50, hertz=7902.13, parts=('B', '', 8)),
    'A#4': dict(val=1, hertz=466.16, parts=('A', '#', 4)),
    'Ab4': dict(val=-1, hertz=415.30, parts=('A', 'b', 4)),
    'Bb4': dict(val=1, hertz=466.16, parts=('B', 'b', 4)),
}


class ToneTest(TestCase):
    def test_invalid_note(self):
        for note in ['A9', 'H4', '4A', 'a4', 'Az4']:
            errmsg = re.escape(
                '%s is not a valid note. notes are A-F, are either normal, '
                'flat (b) or sharp (#) and of octave 0-8' % note
            )
            with self.assertRaisesRegex(Exception, errmsg):
                _convert_args(note, 1)

    def test_note_to_hertz(self):
        for note, val in TEST_NOTES.items():
            params = _convert_args(note, 1.0)
            self.assertAlmostEqual(params.hz, val['hertz'], 2)
