import os.path
from types import ModuleType
import pygame.image
import pygame.mixer


class BaseLoaderModule(ModuleType):

    def __init__(self, path):
        self.path = path
        self.__path__ = [path]
        super().__init__(os.path.basename(path))

    def __getattr__(self, name):
        subdir = os.path.join(self.path, name)
        if os.path.isdir(subdir):
            resource = ImageLoaderModule(subdir)
        else:
            try:
                resource = self.load(name)
            except KeyError as e:
                raise ImportError(*e.args) from None

        setattr(self, name, resource)
        return resource

    def load(self, name):
        p = os.path.join(self.path, name)
        if os.path.exists(p):
            return self.load_(p)

        for ext in self.EXTNS:
            p = os.path.join(self.path, name + '.' + ext)
            if os.path.exists(p):
                return self.load_(p)

        raise KeyError(
            "No {type} found like '{name}'. Are you sure the {type} exists?".format(
                type=self.TYPE,
                name=name
            )
        )


class ImageLoaderModule(BaseLoaderModule):
    EXTNS = ['png', 'gif', 'jpg', 'jpeg', 'bmp']

    def load_(self, path):
        return pygame.image.load(path)


class SoundLoaderModule(BaseLoaderModule):
    EXTNS = ['wav', 'ogg']

    def load_(self, path):
        return pygame.mixer.Sound(path)
