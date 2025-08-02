from fastapi import FastAPI, HTTPException, status
import requests

from app.config import settings
from app.utils import get_languages, get_stars, get_activity_score

app = FastAPI()

PERSONAL_ACCESS_TOKEN = settings.personal_access_token

@app.get("/api/repos/{username}/")
def analyse_profile(username: str, page: int = 1):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f"Bearer {PERSONAL_ACCESS_TOKEN}",
        'X-GitHub-Api-Version': '2022-11-28'
    }
    params = {'page': page}
    repos = requests.get(url, params=params, headers=headers)
    
    if repos.status_code == 404:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if repos.status_code != 200:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, 
            "GitHub API error"
        )

    repos_response = [
        {
            'repository_name': repo['name'],
            'stars': get_stars(username, repo['name']),
            'forks': repo['forks'],
            'languages': get_languages(username, repo['name']),
            'activity_score': get_activity_score(username, repo['name'])
        }
        for repo in repos.json()
    ]

    return {"success": True, "repositories": repos_response}
