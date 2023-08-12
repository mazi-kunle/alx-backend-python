#!/usr/bin/env python3
'''
This is a module
'''
import unittest
from requests import HTTPError
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from fixtures import TEST_PAYLOAD


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, input_a, input_b, expected):
        '''
        a test
        '''
        self.assertEqual(GithubOrgClient.has_license(input_a, input_b),
                         expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''
    a class
    '''
    @classmethod
    def setUpClass(cls) -> None:
        '''
        setup class method
        '''
        payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in payload:
                return Mock(**{'json.return_value': payload[url]})
            return HTTPError

        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        # print(cls.get_patcher)
        cls.get_patcher.start()

    def test_public_repos(self):
        '''a method'''
        self.assertEqual(GithubOrgClient('google').public_repos(),
                         self.expected_repos)

    def test_public_repos_with_license(self):
        '''
        a method
        '''
        self.assertEqual(
            GithubOrgClient('google')
            .public_repos(license='apache-2.0'),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        '''
        teardown class method
        '''
        cls.get_patcher.stop()
