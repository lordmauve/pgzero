import unittest
from unittest import mock
from unittest.mock import patch

from pgzero.storage import Storage


class StorageStaticMethodsTest(unittest.TestCase):
    def test_dict_with_no_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel'}

        result = Storage._get_json_error_keys(obj)
        self.assertIsNone(result)

    def test_dict_with_errors(self):
        obj = {'level': 10, 'player_name': 'Daniel', 'obj': object()}
        expected_result = ("['obj']", type(object()))

        result = Storage._get_json_error_keys(obj)
        self.assertEqual(result, expected_result)

    def test_dict_with_nested_dicts_errors(self):
        subobj0 = {'this_key_fails': object()}
        subobj1 = {'a': 10, 'b': 20, 'c': 30, 'obj': subobj0}
        subobj2 = {'player_name': 'Daniel', 'level': 20, 'states': subobj1}
        obj = {'game': 'my_game', 'state': subobj2}
        expected_result = ("['state']['states']['obj']['this_key_fails']", type(object()))

        result = Storage._get_json_error_keys(obj)
        self.assertEqual(result, expected_result)


class StorageTest(unittest.TestCase):
    @patch('pgzero.storage.os.path.exists')
    def setUp(self, exists_mock):
        exists_mock.return_value = True
        self.storage = Storage()

    def test_get(self):
        with patch('builtins.open', mock.mock_open(read_data='{"a": "hello"}')) as m:
            self.storage.load()
            self.assertEqual(self.storage['a'], 'hello')
