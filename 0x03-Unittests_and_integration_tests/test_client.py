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



#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient including mocking a property
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected URL based on org data."""

        # Known payload to mock the org property
        mock_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch the 'org' property to return mock_payload
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = mock_payload

            client = GithubOrgClient("google")

            # Access the _public_repos_url property
            result = client._public_repos_url

            # Assert that the result matches the mocked repos_url
            self.assertEqual(result, mock_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()


#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient: testing public_repos with patching
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list using mocks."""

        # Payload that get_json should return
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        # Assign the mocked get_json to return our payload
        mock_get_json.return_value = mock_payload

        # Patch the _public_repos_url property to return a dummy URL
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=property) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            # The expected list of repo names
            expected = ["repo1", "repo2", "repo3"]

            # Check that the returned list matches expected
            self.assertEqual(result, expected)

            # Ensure _public_repos_url was accessed exactly once
            mock_url.assert_called_once()

            # Ensure get_json was called exactly once with the mocked URL
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")


if __name__ == "__main__":
    unittest.main()


#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.has_license using parameterized inputs
"""

import unittest
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on repo license."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
