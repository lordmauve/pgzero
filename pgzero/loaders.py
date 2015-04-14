import os.path
from types import ModuleType
import pygame.image
import pygame.mixer


# Root directory for loaders
root = '.'


class ResourceLoader:
    """Abstract resource loader.

    A resource loader is a singleton; resources are loaded from a named
    subdirectory of the global 'root'.

    """
    def __init__(self, subpath):
        self.subpath = subpath

    def root(self):
        return os.path.join(root, self.subpath)

    def load(self, name):
        p = os.path.join(self.root(), name)
        if os.path.exists(p):
            return self.load_(p)

        for ext in self.EXTNS:
            p = os.path.join(root, self.subpath, name + '.' + ext)
            if os.path.exists(p):
                return self.load_(p)

        raise KeyError(
            "No {type} found like '{name}'. "
            "Are you sure the {type} exists?".format(
                type=self.TYPE,
                name=name
            )
        )


class ImageLoader(ResourceLoader):
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']
    TYPE = 'image'

    def load_(self, path):
        return pygame.image.load(path).convert_alpha()


class SoundLoader(ResourceLoader):
    EXTNS = ['wav', 'ogg']
    TYPE = 'sound'

    def load_(self, path):
        return pygame.mixer.Sound(path)


images = ImageLoader('images')
sounds = SoundLoader('sounds')


class LoaderModule(ModuleType):
    def __init__(self, loader):
        self._loader = loader
        self.__path__ = [loader.root()]
        super().__init__(os.path.basename(loader.root()))

    def __getattr__(self, name):
        try:
            resource = self._loader.load(name)
        except KeyError as e:
            raise ImportError(*e.args) from None

        setattr(self, name, resource)
        return resource
