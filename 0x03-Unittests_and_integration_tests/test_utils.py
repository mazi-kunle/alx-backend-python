#!/usr/bin/env python3
'''This is a module'''

import unittest
import requests
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from typing import Any, Dict, Sequence
from unittest.mock import patch, Mock, MagicMock


class TestAccessNestedMap(unittest.TestCase):
    '''
    A test class
    '''
    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict,
                               path: Sequence, expected: Any):
        '''
        test for access_nested_map
        '''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Dict,
                                         path: Sequence):
        '''
        test for access nested map exception
        '''
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''
    A testJson class
    '''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        '''
        test for get_json
        '''
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        mock_get.return_value = mock_response
        self.assertEqual(get_json(test_url),
                         test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    '''A Test Memoize class'''
    def test_memoize(self):
        '''test for memoize'''
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        a = TestClass()

        with patch.object(a, 'a_method') as mock_method:
            mock_method.return_value = 42
            self.assertEqual(a.a_property, 42)
            self.assertEqual(a.a_property, 42)
            mock_method.assert_called_once()
