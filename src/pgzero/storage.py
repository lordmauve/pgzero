import json
import os
import platform
from hashlib import sha1

# For screenshot functionality
from datetime import datetime
import pygame.image


__all__ = ['StorageCorruptionException', 'JSONEncodingException', 'Storage']


class StorageCorruptionException(Exception):
    """The data in the storage is corrupted."""


class JSONEncodingException(Exception):
    """The data in the storage is corrupted."""


# The parameter allows the same function to get the path for save data and screenshots
# on MacOS and Linux.
def _get_platform_pgzero_path(final_dir):
    r"""Get the storage directory for pgzero save data.

    Under Windows, return %APPDATA%\pgzero. Under Linux/MacOS, return
    ~/.config/pgzero/saves.

    """
    if platform.system() == 'Windows':
        try:
            appdata = os.environ['APPDATA']
        except KeyError:
            raise KeyError(
                "Couldn't find the AppData directory for Pygame Zero save "
                "data. Please set the %APPDATA% environment variable."
            )
        # FIXME: Is the windows path intended not to have a saves/screenshots subfolder?
        return os.path.join(appdata, 'pgzero')
    return os.path.expanduser(os.path.join('~', '.config/pgzero', final_dir))

# Moved this function out of Storage to make it reusable for screenshot functionality.
def _ensure_path(path):
    """Checks if the path exists and makes all necessary directories if not."""
    try:
        os.makedirs(path)
    except (IsADirectoryError, PermissionError):
        pass
    except FileExistsError:
        pass


class Storage(dict):
    """Behaves like a dictionary that serialises itself to disk.

    The name of the file will be based on the basename of the script plus
    a hash of the script's path, ensuring that each script on the filesystem
    has a unique save file.

    """
    # The function is given "saves" now to make it behave the same as before
    # when the function always returned a path or save files.
    STORAGE_DIR = _get_platform_pgzero_path("saves")

    # Keep a reference to all defined storages
    storages = []

    def __init__(self, filename=None):
        super().__init__()
        self.loaded = False
        self._save_file = filename
        self.storages.append(self)

    @classmethod
    def save_all(cls):
        """Save all instances of Storage."""
        cls._ensure_save_path()
        for storage in cls.storages:
            storage.save()

    @classmethod
    def _ensure_save_path(cls):
        """Ensure that the directory for all save game data exists."""
        _ensure_path(cls.STORAGE_DIR)

    def _set_filename_from_path(self, file_path):
        """Set the path to save to from the given filename.

        We include the basename of the game script, to help with identifying
        the save data, as well as the sha1 hash of the full path of the file on
        disk, to ensure that every separate game has its own storage.

        """
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)

        fn_hash = sha1(file_path.encode('utf-8')).hexdigest()
        base, _ = os.path.splitext(os.path.basename(file_path))
        self._save_file = '{}-{}.json'.format(base, fn_hash)
        self.load()

    @property
    def path(self):
        """Get the path for data data."""
        if self._save_file is None:
            raise ValueError(
                "Cannot save/load storage as no filename is set."
            )
        return os.path.join(self.STORAGE_DIR, self._save_file)

    def load(self):
        """Load data into the storage from disk.

        This replaces all previous contents of the storage. If there is no save
        file found then the storage will be empty.

        """
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
            self.loaded = True

    def save(self):
        """Save data to disk."""
        if not self and not self.loaded:
            return
        # The save functionality seems to have been broken before this point,
        # since saving manually in the game script did not make sure the save
        # path actually existed. This fixes it.
        Storage._ensure_save_path()
        try:
            data = json.dumps(self)
        except TypeError:
            msgs = [
                "{} - type {}".format(*item)
                for item in self._get_json_error_keys(self)
            ]
            if not msgs:
                # Didn't find an explanation, so let original error propagate
                raise
            raise JSONEncodingException(
                "The following storage entries cannot be stored, because "
                "they are not JSON serializable types:\n{}\n\n"
                "Only the following types of objects are JSON-serialisable: "
                "dict, list/tuple, str, float/int, bool, and None".format(
                    "\n".join(msgs)
                )
            )
        else:
            path = self.path
            with open(path, 'w+') as f:
                f.write(data)
            print("Saved storage to", path)

    # Constants for use with isinstance in _get_json_error_keys()
    JSON_PRIMITIVES = (float, int, str, bool, type(None))
    JSON_SEQ = (list, tuple)
    JSON_MAPPING = dict

    @classmethod
    def _get_json_error_keys(cls, obj, json_path='storage'):
        """Identify the paths with the storage which failed to be JSON encoded.

        Return an iterable of message strings.

        """
        if isinstance(obj, dict):
            # TODO: also check/report that k is a string, as only strings are
            # valid as object keys in JSON.
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


storage = Storage()

# This function is used to create the screenshot instance with the file name
# given by runner.py but save it in the scope of storage.
def _initialize_screenshots(file_path):
    # If the instance already exists, do nothing.
    if "screenshots" in globals():
        return
    # Otherwise, create the instance of the Screenshots class used to
    # take and save screenshots.
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)
    project_name, _ = os.path.splitext(os.path.basename(file_path))

    global screenshots
    screenshots = Screenshots(project_name)


class Screenshots:
    """Class to manage taking screenshots."""
    def __init__(self, project_name):
        self._project_name = project_name
        self._path = _get_platform_pgzero_path("screenshots")

    def take(self, surface):
        # Ensure that the directory for screenshots exists.
        _ensure_path(self._path)

        # Creates the filename, made up of the script name and a timestamp.
        filename = self._project_name + datetime.now().strftime("-%y%m%d-%H%M%S") + ".jpg"
        filepath = os.path.join(self._path, filename)
        # Save the screenshot.
        pygame.image.save(surface, filepath)

