import os.path
from types import ModuleType
import pygame.image


class ImageLoaderModule(ModuleType):
    EXTNS = 'png gif jpg jpeg bmp'.split()

    def __init__(self, path):
        self.path = path
        super().__init__(os.path.basename(path))

    def __getattr__(self, name):
        subdir = os.path.join(self.path, name)
        if os.path.isdir(subdir):
            return ImageLoaderModule(subdir)

        for ext in self.EXTNS:
            p = os.path.join(self.path, name + '.' + ext)
            if os.path.exists(p):
                return self.load_(p)

    def load_(self, path):
        return pygame.image.load(path)
