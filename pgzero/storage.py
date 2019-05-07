import json
import os
import platform


__all__ = ['StorageCorruptionException', 'JSONEncodingException', 'Storage']


class StorageCorruptionException(Exception):
    """The data in the storage is corrupted."""


class JSONEncodingException(Exception):
    """The data in the storage is corrupted."""


class Storage(dict):
    """Behaves like a dictionary with a few extra functions.

    It's possible to load/save the data to disk.

    The name of the file will be the script's name hashed.

    NOTE: If two scripts have the same name, they will load/save from/to
    the same file.
    """

    path = ''

    def __init__(self):
        super().__init__()

        storage_path = self._get_platform_pgzero_path()
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)

    @classmethod
    def set_app_hash(cls, name):
        storage_path = cls._get_platform_pgzero_path()
        cls.path = os.path.join(storage_path, '{}.json'.format(name))

    def load(self):
        """Load data from disk."""
        self.clear()

        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # If no file exists, it's fine
            pass
        except json.JSONDecodeError:
            raise StorageCorruptionException(
                "Storage is corrupted. Couldn't load the data."
            )
        else:
            self.update(data)

    def save(self):
        """Save data to disk."""
        try:
            data = json.dumps(self)
        except TypeError:
            msgs = [
                "{} - type {}".format(*item)
                for item in self._get_json_error_keys(self)
            ]
            raise JSONEncodingException(
                "The following storage entries cannot be stored, because "
                "they are not JSON serializable types:\n{}\n\n"
                "Only the following types of objects are JSON-serialisable: "
                "dict, list/tuple, str, float/int, bool, and None".format(
                    "\n".join(msgs)
                )
            )
        else:
            with open(self.path, 'w+') as f:
                f.write(data)

    # Constants for use with isinstance in _get_json_error_keys()
    JSON_PRIMITIVES = (float, int, str, bool, type(None))
    JSON_SEQ = (list, tuple)
    JSON_MAPPING = dict

    @classmethod
    def _get_json_error_keys(cls, obj, json_path='storage'):
        """Identify the paths with the storage which failed to be JSON encoded.

        Return an iterable of pairs (path, typename).

        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, cls.JSON_PRIMITIVES):
                    continue
                subpath = '{}[{!r}]'.format(json_path, k)
                yield from cls._get_json_error_keys(v, subpath)
        elif isinstance(obj, (list, tuple)):
            for i, value in enumerate(obj):
                if isinstance(value, cls.JSON_PRIMITIVES):
                    continue
                subpath = '{}[{}]'.format(json_path, i)
                yield from cls._get_json_error_keys(value, subpath)
        elif isinstance(obj, cls.JSON_PRIMITIVES):
            return
        else:
            # TODO: Could have a custom JSONEncoder in the future, in which
            # case we would have to actually run json.dumps on it to get the
            # result and possibly even drill down on the parameters we got
            # back, if that object happens to have a list as an attribute, for
            # example.
            t = type(obj)
            if t.__module__ != 'builtins':
                typename = '{t.__module__}.{t.__qualname__}'.format(t=t)
            else:
                typename = t.__qualname__
            yield json_path, typename

    @staticmethod
    def _get_platform_pgzero_path():
        r"""Get the storage directory for pgzero save data.

        Under Windows, return %APPDATA%\pgzero. Under Linux/MacOS, return
        ~/.config/pgzero/saves.

        """
        if platform.system() == 'Windows':
            return os.path.join(os.environ['APPDATA'], 'pgzero')
        return os.path.expanduser(os.path.join('~', '.config/pgzero/saves'))


storage = Storage()
