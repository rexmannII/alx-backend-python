#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from utils import get_json # Assuming get_json is in the utils module
from unittest import TestCase
from utils import memoize # Assuming memoize is in utils module
from parameterized import parameterized
from utils import access_nested_map  # Assuming this is where the function is located

class TestAccessNestedMap(TestCase):
    """Test class for utils.access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """Test accessing values from a nested map."""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({"a": 1}, ("a", "b"), "b"),  # KeyError should be raised because "b" is not in {"a": 1}
        ({}, ("a",), "a"),  # KeyError should be raised because {} is empty
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that a KeyError is raised with the expected message."""

        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the exception message is exactly as expected (the missing key)
        self.assertEqual(str(cm.exception), repr(expected_key))



class TestGetJson(unittest.TestCase):
    """Test class for utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')  # Patch requests.get with a mock
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json correctly returns mocked JSON responses."""

        # Create a mock response object with a json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Set the mock_get to return our mock_response when called
        mock_get.return_value = mock_response

        # Call the function with the test_url
        result = get_json(test_url)

        # Assert that requests.get was called exactly once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the result of get_json is equal to the expected payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for utils.memoize decorator."""

    @patch.object
    def test_memoize(self, mock_a_method):
        """Test memoization behavior to ensure method is called only once."""

        # Define the class with memoized property
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Create an instance of TestClass
        instance = TestClass()

        # Mock a_method to simulate the behavior
        mock_a_method.return_value = 42

        # Call a_property twice
        result1 = instance.a_property  # First call to a_property
        result2 = instance.a_property  # Second call to a_property

        # Ensure a_method is only called once, despite two accesses to a_property
        mock_a_method.assert_called_once()

        # Check that the result from both calls is the same (memoized)
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
