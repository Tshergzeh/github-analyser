import requests

from app.config import settings

PERSONAL_ACCESS_TOKEN = settings.personal_access_token

def get_stars(owner: str, repo: str):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f"Bearer {PERSONAL_ACCESS_TOKEN}",
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.get(
        f'https://api.github.com/repos/{owner}/{repo}/stargazers',
        headers=headers
    )
    return len(response.json())
