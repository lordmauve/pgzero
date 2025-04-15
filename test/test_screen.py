import sys
import unittest
from unittest.mock import patch
from tempfile import TemporaryDirectory
from pathlib import Path
import os
import warnings

import numpy as np
import pygame
import pygame.image
import pygame.surfarray

import pgzero.screen as screen
from pgzero.loaders import set_root, images
from pgzero.rect import Rect, ZRect


ROOT = Path(__file__).parent


def assert_screen_match(computed, name):
    """Check that the image on the screen matches the reference image.

    If the reference image is missing, raise an exception, unless the
    environment variable $W2D_SAVE_REF is given; if given, save current output
    as new reference images. These will need to be checked and committed.

    """
    ref_image = ROOT / 'expected-image' / f'{name}.png'

    if not ref_image.exists():
        if os.environ.get('PGZ_SAVE_REF'):
            warnings.warn(
                f"No reference image exists for {name}; saving new screenshot",
                UserWarning
            )
            pygame.image.save(computed, str(ref_image))
            return
        else:
            raise AssertionError(
                f"No reference image exists for {name}; set $PGZ_SAVE_REF "
                "to create."
            )
    else:
        expected = pygame.image.load(str(ref_image))

    comp_surf = pygame.surfarray.array3d(computed)
    exp_surf = pygame.surfarray.array3d(expected)

    failname = ROOT / 'failed-image' / f'{name}.png'

    if np.allclose(comp_surf, exp_surf, atol=2):
        if failname.exists():
            failname.unlink()
        return

    failname.parent.mkdir(exist_ok=True)

    w, h = computed.get_size()
    out = pygame.Surface(
        (w * 2 + 1, w),
        depth=32,
    )
    out.blit(computed, (0, 0))
    out.blit(expected, (w + 1, 0))
    WHITE = (255, 255, 255)
    FONTHEIGHT = 40
    pygame.draw.line(
        out,
        WHITE,
        (w, 0),
        (w, h),
    )
    font = pygame.font.SysFont(pygame.font.get_default_font(), FONTHEIGHT)
    y = h - FONTHEIGHT
    out.blit(font.render("Computed", True, WHITE), (10, y))
    lbl = font.render("Expected", True, WHITE)
    out.blit(lbl, (w * 2 - 9 - lbl.get_width(), y))
    pygame.image.save(out, str(failname))

    raise AssertionError(
        "Images differ; saved comparison images to {}".format(failname)
    )


class ScreenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialise the display and set loaders to target the current dir."""
        pygame.init()
        cls.surf = pygame.display.set_mode((200, 200))
        set_root(__file__)

    @classmethod
    def tearDownClass(cls):
        """Shut down the display."""
        pygame.display.quit()

    def setUp(self):
        self.screen = screen.Screen()
        self.screen._set_surface(self.surf)
        self.screen.clear()

    def assertImagesAlmostEqual(self, computed, expected):
        """Check that 2 images are approximately equal."""
        comp_surf = pygame.surfarray.array3d(computed)
        exp_surf = pygame.surfarray.array3d(expected)

        if np.allclose(comp_surf, exp_surf, atol=2):
            return

        name = sys._getframe(1).f_code.co_name
        tmpdir = Path(__file__).parent / 'failed-image'
        tmpdir.mkdir(exist_ok=True)
        pygame.image.save(
            computed,
            str(tmpdir / '{}-computed.png'.format(name))
        )
        pygame.image.save(
            expected,
            str(tmpdir / '{}-expected.png'.format(name))
        )

        raise AssertionError(
            "Images differ; saved comparison images to {}".format(tmpdir)
        )

    def test_blit_surf(self):
        """We can blit a surface to the screen."""
        self.screen.blit(images.alien, (0, 0))
        assert_screen_match(self.surf, 'alien_blit')

    def test_blit_name(self):
        """screen.blit() accepts an image name instead of a Surface."""
        self.screen.blit('alien', (0, 0))
        assert_screen_match(self.surf, 'alien_blit')

    def test_fill_gradient(self):
        """We can fill the screen with a gradient."""
        self.screen.fill('black', gcolor='blue')
        assert_screen_match(self.surf, 'gradient')

    def test_line(self):
        yellow = (255, 255, 0)
        """We can draw a line."""
        self.screen.draw.line(start=(0, 50), end=(100, 30), color=yellow, width=9)
        assert_screen_match(self.surf, 'line')

    def test_line_errors(self):
        """draw.line raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.line(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.line([2], yellow)

    def test_circle(self):
        yellow = (255, 255, 0)
        """We can draw a circle."""
        self.screen.draw.circle(pos=(50, 50), radius=50, color=yellow, width=9)
        assert_screen_match(self.surf, 'circle')

    def test_filled_circle(self):
        yellow = (255, 255, 0)
        """We can draw a filled circle."""
        self.screen.draw.filled_circle(pos=(50, 50), radius=50, color=yellow)
        assert_screen_match(self.surf, 'filled_circle')

    def test_circle_errors(self):
        """draw.circle raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.circle(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.circle([2], yellow)

    def test_polygon(self):
        poly = [(0, 99), (49, 0), (99, 99)]
        yellow = (255, 255, 0)
        """We can draw a polygon."""
        self.screen.draw.polygon(poly, yellow)
        assert_screen_match(self.surf, 'polygon')

    def test_filled_polygon(self):
        poly = [(0, 99), (49, 0), (99, 99)]
        yellow = (255, 255, 0)
        """We can draw a filled polygon."""
        self.screen.draw.filled_polygon(poly, yellow)
        assert_screen_match(self.surf, 'filled_polygon')

    def test_polygon_errors(self):
        """draw.polygon raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.polygon(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.polygon([2], yellow)

    def test_rect(self):
        yellow = (255, 255, 0)
        """We can draw a rectangle."""
        self.screen.draw.rect(rect=Rect((20, 20), (100, 100)), color=yellow, width=9)
        assert_screen_match(self.surf, 'rect')

    def test_filled_rect(self):
        yellow = (255, 255, 0)
        """We can draw a filled rectangle."""
        self.screen.draw.filled_rect(rect=Rect((0, 0), (100, 100)), color=yellow)
        assert_screen_match(self.surf, 'filled_rect')

    def test_rect_errors(self):
        """draw.rect raises errors as expected."""
        yellow = (255, 255, 0)
        with self.assertRaises(TypeError):
            self.screen.draw.rect(2, yellow)
        with self.assertRaises(TypeError):
            self.screen.draw.rect([2], yellow)

    def test_wrapped_gradient_text(self):
        """We can draw wrapped gradient text.

        Relates to issue #165 https://github.com/lordmauve/pgzero/issues/165

        """
        self.screen.draw.text(
            'gradient\ntext',
            (0, 0),
            fontname='eunomia_regular',
            fontsize=18,
            color='red',
            gcolor='blue'
        )
        assert_screen_match(self.surf, 'wrapped_gradient_text')

    def test_bounds(self):
        """We can get a bounding rect for the screen."""
        self.assertEqual(
            self.screen.bounds(),
            ZRect(0, 0, 200, 200)
        )

    @patch("sys.platform", "win32")
    @patch.dict("os.environ", {"USERPROFILE": r"c:\Users\user"})
    def test_get_screenshot_path_windows(self):
        r"""Screenshot path on Windows is %USERPROFILE%\Pictures\pgzero."""
        result_path = screen._get_platform_screenshot_path()
        self.assertEqual(result_path,
                         os.path.join(r"c:\Users\user", "Pictures", "pgzero"))

    @patch("sys.platform", "linux")
    @patch.dict("os.environ", {"HOME": "/home/user"})
    def test_get_screenshot_path_linux(self):
        """Screenshot path on Linux or MacOS is ~/Pictures/pgzero."""
        result_path = screen._get_platform_screenshot_path()
        self.assertEqual(result_path,
                         os.path.join("/home/user", "Pictures", "pgzero"))

    @patch("sys.platform", "NOTHING")
    def test_get_screenshot_path_other(self):
        """If OS is not supported, CWD is used for screenshots."""
        result_path = screen._get_platform_screenshot_path()
        self.assertEqual(result_path,
                         os.path.join(os.getcwd(), "pgzero_screenshots"))

    @patch("sys.platform", "NOTHING")
    def test_take_screenshot(self):
        """Screenshot files are created and have the proper extension."""
        with TemporaryDirectory("screenshot_testdir") as td:
            os.chdir(td)
            screen._initialize_screenshots(__file__)
            self.screen.screenshot()
            self.assertEqual(len(os.listdir("pgzero_screenshots")), 1)
            ext = os.listdir("pgzero_screenshots")[0].split(".")[-1]
            self.assertEqual(ext, "png")


if __name__ == '__main__':
    unittest.main()
