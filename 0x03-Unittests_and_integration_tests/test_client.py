# client.py
from typing import Any
from utils import get_json  # Ensure get_json exists

class GithubOrgClient:
    """GithubOrgClient class."""

    def __init__(self, org: str) -> None:
        self.org = org

    def org(self) -> Any:
        """Return JSON payload for the organization."""
        return get_json(f"https://api.github.com/orgs/{self.org}")


#!/usr/bin/env python3
"""
Unit test for client.GithubOrgClient using parameterized and patch decorators
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected result."""

        # Setup mock return value
        mock_get_json.return_value = {"org": org_name}

        # Create client and call org
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert get_json was called once with correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        # Assert the returned value matches mock
        self.assertEqual(result, {"org": org_name})


if __name__ == "__main__":
    unittest.main()
