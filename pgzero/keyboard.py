from collections import defaultdict

from pygame import locals


class Keyboard:
    def __init__(self):
        self.__dict__['d'] = defaultdict(lambda: False)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, key):
        try:
            if key.startswith('K_'):
                key = getattr(locals, key)
            else:
                key = getattr(locals, 'K_' + key)
        except AttributeError:
            raise AttributeError('the key "%s" does not exist' % key)
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value
