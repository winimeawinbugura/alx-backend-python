#!/usr/bin/env python3
"""
Unit tests for access_nested_map with parameterization.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map




class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct return values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """Test KeyError is raised with correct message."""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(str(err.exception), expected_message)








#!/usr/bin/env python3
"""
Utility functions for nested map operations.
"""

from typing import Any, Mapping, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple[str, ...]) -> Any:
    """
    Access a value inside a nested map using a tuple path.

    Args:
        nested_map: A dictionary containing nested dictionaries.
        path: A tuple of keys representing the access path.

    Returns:
        The value found following the path order.

    Raises:
        KeyError: If any key along the path does not exist.
    """
    current = nested_map
    for key in path:
        current = current[key]
    return current


#!/usr/bin/env python3
"""
Unit tests for access_nested_map using parameterization.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct output using parameterized inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
