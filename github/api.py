import os


class GithubObject(object):

    def __init__(self, *args, **kwargs):
        self.root_url = "https://api.github.com"
        self.auth = (os.environ['GITHUB_USERNAME'], os.environ['GITHUB_PUBLIC_ACCESS_TOKEN'])

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
