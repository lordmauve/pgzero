from unittest import TestCase, skip
import pygame
from pgzero.loaders import sounds, set_root, UnsupportedFormat

pygame.init()


class SoundFormatsTest(TestCase):
    """Test that sound formats we cannot open show an appropriate message."""
    @classmethod
    def setUpClass(self):
        set_root(__file__)

    def assert_loadable(self, name):
        s = sounds.load(name)
        l = s.get_length()

        assert 0.85 < l < 1.0, \
            "Failed to correctly load sound (got length %0.1fs)" % l

    def assert_errmsg(self, name, pattern):
        with self.assertRaisesRegex(UnsupportedFormat, pattern):
            sounds.load(name)

    def test_load_22k16bitpcm(self):
        self.assert_loadable('wav22k16bitpcm')

    def test_load_22k8bitpcm(self):
        self.assert_loadable('wav22k8bitpcm')

    def test_load_22kadpcm(self):
        self.assert_loadable('wav22kadpcm')

    def test_load_8k16bitpcm(self):
        self.assert_loadable('wav8k16bitpcm')

    def test_load_8k8bitpcm(self):
        self.assert_loadable('wav8k8bitpcm')

    def test_load_8kadpcm(self):
        self.assert_loadable('wav8kadpcm')

    def test_load_11kgsm(self):
        self.assert_errmsg('wav22kgsm', 'WAV audio encoded as GSM')

    def test_load_11kulaw(self):
        self.assert_loadable('wav22kulaw')

    def test_load_8kmp316(self):
        self.assert_errmsg('wav8kmp316', 'WAV audio encoded as MP3')

    def test_load_8kmp38(self):
        self.assert_errmsg('wav8kmp38', 'WAV audio encoded as MP3')

    def test_load_vorbis1(self):
        """Load OGG Vorbis with .ogg extension."""
        self.assert_loadable('vorbis1')

    def test_load_vorbis2(self):
        """Load OGG Vorbis with .oga extension."""
        self.assert_loadable('vorbis2')
