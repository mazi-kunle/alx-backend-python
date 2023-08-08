#!/usr/bin/env python3
'''This is a module'''

import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Any, Dict, Sequence


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
