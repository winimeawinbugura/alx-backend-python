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

# utils.py
import requests
from typing import Any, Dict

def get_json(url: str) -> Dict[str, Any]:
    """Make an HTTP GET request to the provided URL and return the JSON payload."""
    response = requests.get(url)
    return response.json()


#!/usr/bin/env python3
"""
Unit tests for utils.get_json with mocked HTTP calls
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json

class TestGetJson(unittest.TestCase):
    """Test class for utils.get_json function."""

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected payload.
        Patch requests.get so no actual HTTP request is made.
        """
        # Configure the mock to return a Mock object with a .json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert the function output matches the test_payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()




# utils.py
from functools import wraps
from typing import Callable

def memoize(fn: Callable) -> Callable:
    """Decorator that caches a method's return value."""
    attr_name = "_memoized_value"

    @wraps(fn)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return wrapper


#!/usr/bin/env python3
"""
Unit test for the utils.memoize decorator
"""

import unittest
from unittest.mock import patch
from utils import memoize

class TestMemoize(unittest.TestCase):
    """Test class for utils.memoize decorator."""

    def test_memoize(self):
        """Test that a memoized method only calls the original method once."""

        class TestClass:
            """Sample class to test memoization."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_obj = TestClass()

        # Patch 'a_method' on test_obj
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
