from github import Organization, Repository


if __name__ == "__main__":
    # let's take an example of Google
    org = Organization('google')
    top_repos = org.top_repos_by_fork(5)

    if not top_repos:
        print "Sorry! This organization has no public repos."
        exit()

    print "REPOSITORY | NO_FORKS \n"
    for repo in top_repos:
        current_repo = Repository(repo)
        print repo, top_repos[repo]

        print "contributor_name | no_commits"
        contributor_commits = current_repo.top_contributors_by_commits(3)
        for contributor in contributor_commits:
            print contributor, contributor_commits[contributor]

        print "\n"
