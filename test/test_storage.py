import unittest
from unittest import mock
from unittest.mock import patch

from pgzero.storage import Storage
from pgzero.rect import ZRect


class StorageStaticMethodsTest(unittest.TestCase):
    def test_dict_with_no_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel'}

        result = list(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [])

    def test_dict_with_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel', 'obj': object()}

        result = list(Storage._get_json_error_keys(obj))
        self.assertEqual(
             result,
             [("storage['obj']", "object")]
        )

    def test_dict_with_nested_dicts_errors(self):
        subobj0 = {'this_key_fails': object()}
        subobj1 = {'a': 10, 'b': {1, 2, 3}, 'c': 30, 'obj': subobj0}
        subobj2 = {'player_name': 'Daniel', 'level': 20, 'states': subobj1}
        obj = {'game': 'my_game', 'state': subobj2}

        result = sorted(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [
            ("storage['state']['states']['b']", 'set'),
            ("storage['state']['states']['obj']['this_key_fails']", 'object'),
        ])

    def test_invalid_list_item(self):
        """We can report the index of an unserialisable list item."""
        obj = {'items': [1, 5, ZRect(0, 0, 10, 10)]}

        result = sorted(Storage._get_json_error_keys(obj))
        self.assertEqual(result, [
            ("storage['items'][2]", 'pgzero.rect.ZRect'),
        ])


class StorageTest(unittest.TestCase):
    @patch('pgzero.storage.os.path.exists')
    def setUp(self, exists_mock):
        exists_mock.return_value = True
        self.storage = Storage('asdf')

    @patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}'))
    def test_get(self):
        self.storage.load()
        self.assertEqual(self.storage['a'], 'hello')
