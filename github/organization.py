from collections import OrderedDict

import requests
import grequests

from .GithubObject import GithubObject


class Organization(GithubObject):
    """To provide abstractions around organizations."""

    def __init__(self, org_name):
        super(Organization, self).__init__()

        self.organization_url = self.get_organization_url(org_name)
        self.repos_url = self.get_organization_repos_url(org_name)
        self.repo_data = None

    def add_repo_list_data(self, repo_list):
        self.repo_data += repo_list

    def has_public_repos(self):
        org_data = requests.get(self.organization_url, auth=self.auth).json()
        if 'public_repos' in org_data and org_data['public_repos'] > 0:
            return True
        return False

    def fetch_repos(self):
        """Fetch the json data of all repos in the organization.

        This method uses asynchronous processing using `grequests.map`.

        Note: Can be changed to hook based update using `grequests.send` with `timeout` if a time constraint 
        is added to repo fetching.
        """
        if not self.repo_data:
            self.repo_data = []

        org_data = requests.get(self.organization_url, auth=self.auth).json()
        no_repos = org_data['public_repos']
        results_per_page = 30

        last_page = 0 if (no_repos % results_per_page) == 0 else 1
        no_pages = (no_repos / results_per_page) + last_page

        urls_to_fetch = [self.get_paginated_url(self.repos_url, page_no) for page_no in xrange(1, no_pages + 1)]
        request_pool = [grequests.get(each_url, auth=self.auth) for each_url in urls_to_fetch]

        # this will take couple of seconds to process huge list of repos for big organizations.
        # for most other organizations, this is is almost instant
        responses = grequests.map(request_pool)
        for response in responses:
            self.add_repo_list_data(response.json())

    def top_repos_by_fork(self, repos_needed):
        """Fetch top repos sorted by no of forks.

        Note: Excluding the repositories which have been forked by Google itself.
        """
        # check if this organization has any public repos
        if not self.has_public_repos():
            return None

        if not self.repo_data:
            # update repos if data is empty
            self.fetch_repos()

        source_repos = filter(lambda x: not x['fork'], self.repo_data)
        sorted_source_repos = sorted(source_repos, key=lambda x: x['forks_count'], reverse=True)[:repos_needed]
        repos_forks = OrderedDict((repo_data['full_name'], repo_data['forks_count']) for repo_data in sorted_source_repos)

        return repos_forks
