import hashlib

import requests

from app.config import settings

PERSONAL_ACCESS_TOKEN = settings.personal_access_token

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f"Bearer {PERSONAL_ACCESS_TOKEN}",
    'X-GitHub-Api-Version': '2022-11-28'
}

def make_cache_key(username: str, page: int):
    raw_key = f"username:{username};page:{page}"
    return hashlib.md5(raw_key.encode()).hexdigest()

def get_stars(owner: str, repo: str):
    stars = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/stargazers',
        headers=headers
    )
    return len(stars.json())


def get_languages(owner: str, repo: str):
    languages_response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/languages',
        headers=headers
    )
    languages = list(languages_response.json().keys())
    return languages

def get_activity_score(owner: str, repo: str):
    number_of_commits = get_number_of_commits(owner, repo)
    number_of_pull_requests = get_number_of_pull_requests(owner, repo)
    number_of_issues = get_number_of_issues(owner, repo)
    number_of_stars = get_stars(owner, repo)
    activity_score = (number_of_commits * 0.5) + (number_of_pull_requests * 0.3) + (number_of_issues * 0.1) + (number_of_stars * 0.1)
    return activity_score

def get_total_from_paginated_response(response):
    if 'link' in response.headers:
        links = response.headers["Link"].split(",")
        last_link = [link for link in links if 'rel="last"' in link]
        last_url = last_link[0].split(";")[0].strip()[1:-1]
        last_page = int(last_url.split("page=")[-1])
        last_page_response = requests.get(last_url, headers=headers)
        last_page_response_count = len(last_page_response.json())
        total_count = (last_page - 1) * 30 + last_page_response_count
        return total_count
    return len(response.json())

def get_number_of_commits(owner: str, repo: str):
    commits = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/commits',
        headers=headers
    )
    return get_total_from_paginated_response(commits)

def get_number_of_pull_requests(owner: str, repo: str):
    pull_requests = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/pulls',
        headers=headers
    )
    return get_total_from_paginated_response(pull_requests)

def get_number_of_issues(owner: str, repo: str):
    issues = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/issues',
        headers=headers
    )
    return get_total_from_paginated_response(issues)
