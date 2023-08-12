#!/usr/bin/env python3
'''
This is a module
'''
import unittest
import requests
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, Mock, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    '''
    a test class
    '''
    @parameterized.expand([
        ('google', {'payload': True}),
        ('abc', {'payload': False})
    ])
    @patch('requests.get')
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_getJson, mock_get):
        '''
        a test method
        '''
        # mock request.get
        mock_getResponse = Mock()
        mock_getResponse.json.return_value = expected
        mock_get.return_value = mock_getResponse

        # mock get_json
        mock_getJson.return_value = mock_get().json()

        test = GithubOrgClient(org_name)
        self.assertEqual(test.org, expected)
        mock_getJson.assert_called_once_with(test.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        '''
        a test method
        '''
        test = GithubOrgClient('google')

        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos"
            }
            self.assertEqual(
                test._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_getJson):
        '''
        a test method
        '''
        payload = [{
            "login": "google",
            "id": 1342004,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNDIwMDQ=",
            "url": "https://api.github.com/orgs/google",
            "repos_url": "https://api.github.com/orgs/google/repos",
            "events_url": "https://api.github.com/orgs/google/events",
            "hooks_url": "https://api.github.com/orgs/google/hooks",
            "issues_url": "https://api.github.com/orgs/google/issues",
            "members_url": "https://api.github.com/orgs/google/members",
            "public_members_url": "https://api.github.com/orgs/google",
            "avatar_url": "https://avatars.githubusercontent.com/u",
            "description": "Google ❤️ Open Source",
            "name": "Google",
            "company": None,
            "blog": "https://opensource.google/",
            "location": None,
            "email": "opensource@google.com",
            "twitter_username": "GoogleOSS",
            "is_verified": True,
            "has_organization_projects": True,
            "has_repository_projects": True,
            "public_repos": 2531,
            "public_gists": 0,
            "followers": 27361,
            "following": 0,
            "html_url": "https://github.com/google",
            "created_at": "2012-01-18T01:30:18Z",
            "updated_at": "2021-12-30T01:40:20Z",
            "archived_at": None,
            "type": "Organization"
        }]
        mock_getJson.return_value = payload
        test = GithubOrgClient('google')

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock:
            mock.return_value = payload[0]['repos_url']
            self.assertEqual(test.public_repos(), ['Google'])
            mock_getJson.assert_called_once()
            mock.assert_called_once()
