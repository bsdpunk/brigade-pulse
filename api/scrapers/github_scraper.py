import json

import requests

from api.models import GitHubRepository, GitHubUser, Project
from api.models.github.github_repository import GitHubRepositoryContributor
from api.snapshots.github_snapshots import GitHubRepositorySnapshot, GitHubContributorSnapshot
from settings import GITHUB_TOKEN


def scrape_github_repos_for_all_projects():
    projects = Project.objects.all()
    for project in projects:
        if project.code_url and 'github' in project.code_url:
            owner_and_repo_string = project.code_url.split('github.com/')[-1]
            response = requests.get('https://api.github.com/repos/{}?access_token={}'.format(owner_and_repo_string,
                                                                                             GITHUB_TOKEN))
            if response.status_code == 200:
                repo_json = json.loads(response.content)
                github_repository = GitHubRepository.objects.filter(id=repo_json['id']).first()
                if not github_repository:
                    github_repository = GitHubRepository()
                github_repository.id = repo_json['id']
                github_repository.name = repo_json['name']
                github_repository.description = repo_json['description']
                github_repository.language = repo_json['language']
                github_repository.homepage = repo_json['homepage']
                github_repository.stargazers_count = repo_json['stargazers_count']
                github_repository.watchers_count = repo_json['watchers_count']
                github_repository.forks_count = repo_json['forks_count']
                github_repository.open_issues = repo_json['open_issues']
                github_repository.created_at = repo_json['created_at']
                github_repository_owner = GitHubUser.objects.filter(name=repo_json['owner']['login']).first()
                if not github_repository_owner:
                    github_repository_owner = GitHubUser()
                github_repository_owner.name = repo_json['owner']['login']
                github_repository_owner.avatar_url = repo_json['owner']['avatar_url']
                github_repository_owner.save()
                github_repository.owner = github_repository_owner
                github_repository.save()
                GitHubRepositorySnapshot().create_snapshot(github_repository)
                project.github_repository = github_repository
                project.save()
                response = requests.get(
                    'https://api.github.com/repos/{}/contributors?access_token={}'.format(owner_and_repo_string,
                                                                                          GITHUB_TOKEN))
                if response.status_code == 200:
                    contributors_json = json.loads(response.content)
                    for contributor_json in contributors_json:
                        contributor = GitHubUser.objects.filter(name=contributor_json['login']).first()
                        if not contributor:
                            contributor = GitHubUser()
                        contributor.name = contributor_json['login']
                        contributor.avatar_url = contributor_json['avatar_url']
                        contributor.save()
                        github_contributor = GitHubRepositoryContributor.objects.filter(repository=github_repository,
                                                                                        contributor=contributor).first()
                        if not github_contributor:
                            github_contributor = GitHubRepositoryContributor()
                        github_contributor.contributor = contributor
                        github_contributor.repository = github_repository
                        github_contributor.contributions = contributor_json['contributions']
                        github_contributor.save()
                        GitHubContributorSnapshot().create_snapshot(github_contributor)
            else:
                print 'ERROR'
