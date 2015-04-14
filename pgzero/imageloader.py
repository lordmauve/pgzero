import os.path
from types import ModuleType
import pygame.image


class ImageLoaderModule(ModuleType):
    EXTNS = 'png gif jpg jpeg bmp'.split()

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
            "No image found like '%s'. Are you sure the image exists?" % name
        )

    def load_(self, path):
        return pygame.image.load(path)
