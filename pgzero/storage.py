import json
import os
import platform
import logging


logger = logging.getLogger(__name__)


__all__ = ['StorageCorruptionException', 'JSONEncodingException', 'Storage']


class StorageCorruptionException(Exception):
    """The data in the storage is corrupted."""


class JSONEncodingException(Exception):
    """The data in the storage is corrupted."""


class Storage(dict):

    path = ''

    """Behaves like a dictionary with a few extra functions.

    It's possible to load/save the data to disk.

    The name of the file will be the script's name hashed.

    NOTE: If two scripts have the same name, they will load/save from/to
    the same file.
    """
    def __init__(self):
        dict.__init__(self)

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
            logger.debug('No file to load data from.')
        except json.JSONDecodeError:
            msg = 'Storage is corrupted. Couldn\'t load the data.'
            logger.error(msg)
            raise StorageCorruptionException(msg)
        else:
            self.update(data)

    def save(self):
        """Save data to disk."""
        try:
            data = json.dumps(self)
        except TypeError:
            json_path, key_type_obj = self._get_json_error_keys(self)
            msg = 'The following entry couldn\'t be JSON serialized: storage{} of type {}'
            msg = msg.format(json_path, key_type_obj)
            logger.error(msg)
            raise JSONEncodingException(msg)
        else:
            with open(self.path, 'w+') as f:
                f.write(data)

    @classmethod
    def _get_json_error_keys(cls, obj, json_path=''):
        """Work out which part of the storage failed to be JSON encoded.

        This function returns None if there is no error.
        """

        if type(obj) in (float, int, str, bool):
            return None
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                result = cls._get_json_error_keys(value, '{}[{}]'.format(json_path, i))
                if result is not None:
                    return result
        elif isinstance(obj, dict):
            for k, v in obj.items():
                result = cls._get_json_error_keys(v, '{}[\'{}\']'.format(json_path, k))
                if result is not None:
                    return result
        else:
            # TODO: Could have a custom JSONEncoder in the future, in which case we would
            # have to actually run json.dumps on it to get the result and possibly even
            # drill down on the parameters we got back, if that object happens to have
            # a list as an attribute, for example.
            return (json_path, type(obj))

        # Explicitly returning None for the sake of code readability
        return None

    @staticmethod
    def _get_platform_pgzero_path():
        """Attempts to get the right directory in Windows/Linux.MacOS"""
        if platform.system() == 'Windows':
            return os.path.join(os.environ['APPDATA'], 'pgzero')
        return os.path.expanduser(os.path.join('~', '.config/pgzero/saves'))


storage = Storage()
