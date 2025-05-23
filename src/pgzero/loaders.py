import os
import os.path
import sys

import pygame.image
import pygame.mixer

from . import ptext


# Root directory for loaders
# This is modified by calling set_root(), which is called by the game runner.
root = '.'


def set_root(path):
    """Configure all loaders to load from the given root.

    path may be a file (such as a Python source file), in which case the root
    is set to its containing directory.

    """
    global root
    path = os.path.abspath(path)
    if os.path.isdir(path):
        root = path
    else:
        root = os.path.dirname(path)
    sys.path.insert(0, root)


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
        self._subpath = subpath
        self._cache = {}
        self._have_root = False

    def validate_root(self, name):
        r = self._root()
        self._have_root = os.path.exists(r)
        if self._have_root:
            validate_compatible_path(r)
        else:
            raise KeyError(
                "No '{subpath}' directory found to load {type} "
                "'{name}'.".format(
                    subpath=self._subpath, type=self.TYPE, name=name
                )
            )

    def _root(self):
        return os.path.join(root, self._subpath)

    @staticmethod
    def cache_key(name, args, kwargs):
        kwpairs = sorted(kwargs.items())
        return (name, args, tuple(kwpairs))

    def load(self, name, *args, **kwargs):
        key = self.cache_key(name, args, kwargs)
        if key in self._cache:
            return self._cache[key]

        if not self._have_root:
            self.validate_root(name)
        p = os.path.join(self._root(), name)

        if not os.path.isfile(p):
            for ext in self.EXTNS:
                p = os.path.join(self._root(), name + '.' + ext)
                if os.path.exists(p):
                    break
            else:
                raise KeyError(
                    "No {type} found like '{name}'. "
                    "Are you sure the {type} exists?".format(
                        type=self.TYPE,
                        name=name
                    )
                )

        validate_compatible_path(p)
        res = self._cache[key] = self._load(p, *args, **kwargs)
        return res

    def unload(self, name, *args, **kwargs):
        key = self.cache_key(name, args, kwargs)
        if key in self._cache:
            del self._cache[key]

    def unload_all(self):
        self._cache.clear()

    def __getattr__(self, name):
        p = os.path.join(self._root(), name)
        if os.path.isdir(p):
            resource = self.__class__(os.path.join(self._subpath, name))
        else:
            try:
                resource = self.load(name)
            except KeyError as e:
                raise AttributeError(*e.args) from None

        setattr(self, name, resource)
        return resource

    def __dir__(self):
        standard_attributes = [key for key in self.__dict__.keys()
                               if not key.startswith("_")]
        resources = os.listdir(self._root())
        resource_names = [os.path.splitext(r) for r in resources]
        loadable_names = [name for name, ext in resource_names
                          if name.isidentifier() and ext[1:] in self.EXTNS]
        return standard_attributes + loadable_names


class ImageLoader(ResourceLoader):
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp', 'webp']
    TYPE = 'image'

    def _load(self, path):
        return pygame.image.load(path).convert_alpha()

    def __repr__(self):
        return "<Images images={}>".format(self.__dir__())


class UnsupportedFormat(Exception):
    """The resource was not in a supported format."""


class SoundLoader(ResourceLoader):
    EXTNS = ['wav', 'ogg', 'oga']
    TYPE = 'sound'

    def _load(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as err:
            if not err.args[0].startswith((
                'Unable to open file',
                'Unknown WAVE format tag',
                'MPEG formats not supported',
            )):
                raise
            from .soundfmt import identify
            try:
                fmt = identify(path)
            except Exception:
                pass
            else:
                raise UnsupportedFormat("""
'{0}' is not in a supported audio format.

It appears to be:

    {1}

Pygame supports only uncompressed WAV files (PCM or ADPCM) and compressed
Ogg Vorbis files. Try re-encoding the sound file, for example using Audacity:

    http://audacityteam.org/
""".format(path, fmt).strip()) from None
            raise

    def __repr__(self):
        try:
            sound_list = self.__dir__()
        except OSError:
            sound_list = []
        return "<Sounds sounds={}>".format(sound_list)


class FontLoader(ResourceLoader):
    EXTNS = ['ttf']
    TYPE = 'font'

    def _load(self, path, fontsize=None):
        return pygame.font.Font(path, fontsize or ptext.DEFAULT_FONT_SIZE)


images = ImageLoader('images')
sounds = SoundLoader('sounds')
fonts = FontLoader('fonts')


def getfont(
        fontname=None,
        fontsize=None,
        sysfontname=None,
        bold=None,
        italic=None,
        underline=None):
    """Monkey-patch for ptext.getfont().

    This will use our loader and therefore obey our case validation, caching
    and so on.

    """
    fontname = fontname or ptext.DEFAULT_FONT_NAME
    fontsize = fontsize or ptext.DEFAULT_FONT_SIZE

    key = (
        fontname,
        fontsize,
        sysfontname,
        bold,
        italic,
        underline
    )

    if key in ptext._font_cache:
        return ptext._font_cache[key]

    if fontname is None:
        font = ptext._font_cache.get(key)
        if font:
            return font
        font = pygame.font.SysFont(sysfontname, fontsize)
    else:
        font = fonts.load(fontname, fontsize)

    if bold is not None:
        font.set_bold(bold)
    if italic is not None:
        font.set_italic(italic)
    if underline is not None:
        font.set_underline(underline)

    ptext._font_cache[key] = font
    return font


ptext.getfont = getfont
