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
