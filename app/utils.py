import requests

from app.config import settings

PERSONAL_ACCESS_TOKEN = settings.personal_access_token

headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f"Bearer {PERSONAL_ACCESS_TOKEN}",
    'X-GitHub-Api-Version': '2022-11-28'
}

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