from collections import OrderedDict

import requests

from .GithubObject import GithubObject


class Repository(GithubObject):
    """To provide abstraction around a repository."""

    def __init__(self, full_repo_name):
        super(Repository, self).__init__()

        self.repo_url = self.get_repo_url(full_repo_name)
        self.contributor_url = self.get_contributor_url(full_repo_name)
        self.contributor_data = None

    def fetch_contributors(self):
        self.contributor_data = requests.get(self.contributor_url, auth=self.auth).json()

    def top_contributors_by_commits(self, no_of_contributors):
        """Top contributors sorted by commits.

        This data can be outdated according to Github: https://developer.github.com/v3/repos/#list-contributors
        """
        if not self.contributor_data:
            self.fetch_contributors()

        top_contributors = self.contributor_data[:no_of_contributors]
        contributors_commits = OrderedDict((contributor['login'], contributor['contributions'])
                                           for contributor in top_contributors)

        return contributors_commits
