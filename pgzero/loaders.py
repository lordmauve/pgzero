import os.path
from types import ModuleType
import pygame.image
import pygame.mixer

from . import ptext


# Root directory for loaders
root = '.'


class InvalidCase(Exception):
    """Indicate case errors early so they don't bite cross-platform users."""

try:
    import win32api
except ImportError:
    def real_path(path):
        return path
else:
    def real_path(path):
        """Get the real capitalisation of a path on Windows."""
        if not os.path.exists(path):
            return path
        return win32api.GetLongPathNameW(win32api.GetShortPathName(path))


def validate_lowercase(relpath):
    if relpath.lower() != relpath:
        raise InvalidCase(
            "%r is not lower case.\n"
            "You must use lower case filenames. This is to avoid "
            "portability problems when run on another operating system "
            "(because filenames on some operating systems are case-"
            "sensitive and others are not)." % relpath

        )


def validate_compatible_path(path):
    """Validate that the given path can be loaded cross-platform."""
    relpath = os.path.relpath(path, root)
    validate_lowercase(relpath)

    real = real_path(os.path.join(root, relpath))
    real_rel = os.path.relpath(real, root)

    if real_rel != relpath:
        raise InvalidCase(
            "%s is mis-capitalised on disk as %r.\nYou should rename it to be "
            "correctly lowercase, for cross-platform portability." % (
                relpath, real_rel
            )
        )


class ResourceLoader:
    """Abstract resource loader.

    A resource loader is a singleton; resources are loaded from a named
    subdirectory of the global 'root'. The `.load()` method actually loads
    a resource.

    Additionally, attribute access can be used to access and cache resources.
    Dotted paths can be used to traverse directories.

    """
    def __init__(self, subpath):
        self.subpath = subpath
        self.have_root = False

    def validate_root(self, name):
        r = self._root()
        self.have_root = os.path.exists(r)
        if self.have_root:
            validate_compatible_path(r)
        else:
            raise KeyError(
                "No '{subpath}' directory found to load {type} "
                "'{name}'.".format(
                    subpath=self.subpath, type=self.TYPE, name=name
                )
            )

    def _root(self):
        return os.path.join(root, self.subpath)

    def load(self, name, *args, **kwargs):
        if not self.have_root:
            self.validate_root(name)
        p = os.path.join(self._root(), name)

        if os.path.isfile(p):
            validate_compatible_path(p)
            return self._load(p, *args, **kwargs)

        for ext in self.EXTNS:
            p = os.path.join(self._root(), name + '.' + ext)
            if os.path.exists(p):
                validate_compatible_path(p)
                return self._load(p, *args, **kwargs)

        raise KeyError(
            "No {type} found like '{name}'. "
            "Are you sure the {type} exists?".format(
                type=self.TYPE,
                name=name
            )
        )

    def __getattr__(self, name):
        p = os.path.join(self._root(), name)
        if os.path.isdir(p):
            resource = self.__class__(os.path.join(self.subpath, name))
        else:
            try:
                resource = self.load(name)
            except KeyError as e:
                raise AttributeError(*e.args) from None

        setattr(self, name, resource)
        return resource


class ImageLoader(ResourceLoader):
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'

    def _load(self, path):
        return pygame.image.load(path).convert_alpha()


class SoundLoader(ResourceLoader):
    EXTNS = ['wav', 'ogg']
    TYPE = 'sound'

    def _load(self, path):
        return pygame.mixer.Sound(path)


class FontLoader(ResourceLoader):
    EXTNS = ['ttf']
    TYPE = 'font'

    def _load(self, path, fontsize):
        return pygame.font.Font(path, fontsize)


images = ImageLoader('images')
sounds = SoundLoader('sounds')
fonts = FontLoader('fonts')


def getfont(fontname, fontsize):
    """Monkey-patch for ptext.getfont().

    This will use our loader and therefore obey our case validation and so
    on.

    """
    fontname = fontname or ptext.DEFAULT_FONT_NAME
    fontsize = fontsize or ptext.DEFAULT_FONT_SIZE

    key = fontname, fontsize
    f = ptext._font_cache.get(key)
    if f:
        return f
    if fontname is None:
        f = pygame.font.Font(fontname, fontsize)
    else:
        f = fonts.load(fontname, fontsize)
    ptext._font_cache[key] = f
    return f

ptext.getfont = getfont
