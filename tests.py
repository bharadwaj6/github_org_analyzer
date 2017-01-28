import unittest

from github import Organization


class TestUrlMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUrlMethods, self).__init__(*args, **kwargs)

        self.org_with_repos = Organization('google')
        self.org_without_repos = Organization('abc')

    def test_organization_url(self):
        self.assertEqual(self.org_with_repos.get_organization_url('google'), 'https://api.github.com/orgs/google')

    def test_repository_url(self):
        self.assertEqual(self.org_with_repos.get_repo_url('google/material-design-icons'),
                         "https://api.github.com/repos/google/material-design-icons")

    def test_empty_org_repos(self):
        self.assertEqual(self.org_without_repos.has_public_repos(), False)

    def test_org_with_repos(self):
        self.assertEqual(self.org_with_repos.has_public_repos(), True)


if __name__ == '__main__':
    unittest.main()
