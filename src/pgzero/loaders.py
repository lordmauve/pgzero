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

# New function to validate animation directory paths.
def validate_animation_paths(path):
    """Validate that the given directory path contains proper files for
    an animation.
    """
    # First, validate the directory path itself.
    validate_compatible_path(path)
    
    dirname = os.path.basename(path)
    warned_dirname = False
    warned_directory = False
    warned_filenames = False
    warned_numbering = False
    warned_no_numbers = False
    warned_extension = False

    # Validate all animation frames (all files in the directory).
    files = sorted(os.listdir(path))
    # Variables to check consistency of naming across files.
    last_anim_name = None
    last_number = None
    last_extension = None
    for f in files:
        # Ignore directories present and give a warning if so.
        if not os.path.isfile(os.path.join(path, f)):
            if not warned_directory:
                print("WARNING: Directory {} found instead of file. Directories in "
                      "animation folders are ignored.".format(f))
                warned_directory = True
            continue

        # Split the filename into its parts and examine them individually.
        basename, extension = f.split(".")
        # Warn if not all files have the same file type.
        if last_extension and last_extension != extension and not warned_extension:
            print("WARNING: Extension of file {} does not match last extension {}. "
                  "Having different file types in one animation is strongly "
                  "discouraged.".format(f, last_extension))
            warned_extension = True

        if "_" in basename:
            anim_name, text_number = basename.rsplit("_", 1)
            # Warn if not all files have the same name before numbering.
            if last_anim_name and last_anim_name != anim_name and not warned_filenames:
                print("WARNING: Filename before numbering {} does not match last "
                      "filename without numbering {}. Consider naming files "
                      "consistently.".format(anim_name, last_anim_name))
                warned_filenames = True
            # Check if the filename ends in a number and warn if not.
            try:
                # If there is a number, check if the sorting of files has produced
                # the correct order of frames.
                number = int(text_number)
                if last_number and number != last_number + 1 and not warned_numbering:
                    print("WARNING: Number of current file ({}) does not follow "
                          "number of last file ({}). Animation frames could be "
                          "missing or with more than 10 frames, numbering could "
                          "produce wrong file order.".format(number, last_number))
                    warned_numbering = True
            except:
                number = None
                if not warned_no_numbers:
                    print("WARNING: Filename {} does not end in a number. Order "
                          "of frames could be wrong.".format(basename))
                    warned_no_numbers = True
            # Check if the filename matches the directory name.
            if anim_name != dirname and not warned_dirname:
                print("WARNING: Filename {} without numbering does not match "
                      "directory name {}.".format(anim_name, dirname))
                warned_dirname = True
        
            # Update last name and last number if there was a valid number.
            last_anim_name = anim_name
            if number:
                last_number = number

        # Update last extension.
        last_extension = extension
        # Validate like any other image file.
        validate_compatible_path(os.path.join(path, f))

    # If any specific warning was given, also give general best practis for
    # naming animation frames.
    if any((warned_dirname, warned_directory, warned_filenames, warned_numbering, 
           warned_no_numbers, warned_extension)):
        print("WARNING SUMMARY: Checking the animation directory revealed "
              "problems that could interfere with correct ingest of animation "
              "frames.\nThe following is suggested best practise:\n\t- Name "
              "animation frames in animation directory DIR as follows: "
              "DIR_NUMBER.EXTENSION.\n\t- Make sure all files are named after "
              "the same pattern.\n\t- Make sure all files are of the same "
              "file type.\n\t- Make sure frames are numbered correctly.\n\t- "
              "If there are 10 or more frames, begin counting with 00 or 01 "
              "instead of just 0 or 1.")


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

        # New if-else to separate dealing with animation loading vs. 
        # non-animation loading.
        if os.path.isdir(p) and self.TYPE == "animation":
            # Validate the animation directory.
            validate_animation_paths(p)
            # With a given directory, the path to load does not 
            # need to be changed here.
        else:
            # Handling of non-animations stays the same.
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
            
            # Validation of the directory has already occurred in 
            # validate_animation_paths() so it's not necessary to
            # call validate_compatible_path() again here.
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


# New class to handle loading of animations
class AnimationLoader(ResourceLoader):
    # Extensions are the same as for ImageLoader as animations are made 
    # up of individual images.
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'animation'

    def _load(self, path):
        # Get paths to all files in the directory
        files = sorted([f_path for f in os.listdir(path) 
                        if os.path.isfile(
                        (f_path := os.path.join(path, f)))])
        # Load all images as Pygame surfaces and return a tuple of frames.
        frames = []
        for f in files:
            frames.append(pygame.image.load(f).convert_alpha())
        return tuple(frames)

    def __repr__(self):
        return "<Animations animations={}>".format(self.__dir__())


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
animations = AnimationLoader('animations')
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

