import os


class GithubObject(object):
    """Used as a container to keep common github data such as authentication and to return different API urls."""

    def __init__(self, *args, **kwargs):
        self.root_url = "https://api.github.com"
        if 'GITHUB_USERNAME' in os.environ and 'GITHUB_PUBLIC_ACCESS_TOKEN' in os.environ:
            self.auth = (os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PUBLIC_ACCESS_TOKEN'])
        else:
            self.auth = None

    def get_organization_url(self, org_name):
        return self.root_url + '/orgs/' + str(org_name)

    def get_organization_repos_url(self, org_name):
        return self.root_url + '/orgs/' + str(org_name) + '/repos'

    def get_repo_url(self, full_repo_name):
        return self.root_url + '/repos/' + str(full_repo_name)

    def get_paginated_url(self, existing_url, page_no):
        return existing_url + '?page=' + str(page_no)

    def get_contributor_url(self, full_repo_name):
        return self.root_url + '/repos/' + full_repo_name + '/contributors'
