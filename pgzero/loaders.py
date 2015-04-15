import os.path
from types import ModuleType
import pygame.image
import pygame.mixer


# Root directory for loaders
root = '.'


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

    def _root(self):
        return os.path.join(root, self.subpath)

    def load(self, name):
        p = os.path.join(self._root(), name)
        if os.path.exists(p):
            return self._load(p)

        for ext in self.EXTNS:
            p = os.path.join(self._root(), name + '.' + ext)
            if os.path.exists(p):
                return self._load(p)

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


images = ImageLoader('images')
sounds = SoundLoader('sounds')
