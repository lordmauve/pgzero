from collections import defaultdict

from pygame import locals


class Keyboard(object):
    def __init__(self):
        self.d = defaultdict(lambda: False)

    def __getattr__(self, key):
        if key.startswith('K_'):
            key = getattr(locals, key)
        else:
            key = getattr(locals, 'K_' + key)
        return self.d[key]

    def __setattr__(self, key, value):
        self.d[key] = value

    def __getitem__(self, key):
        if key.startswith('K_'):
            key = getattr(locals, key)
        else:
            key = getattr(locals, 'K_' + key)
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value
