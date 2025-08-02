import json

from fastapi import FastAPI, HTTPException, status
import requests
import redis

from app.config import settings
from app.utils import get_languages, get_stars, get_activity_score, make_cache_key

app = FastAPI()

PERSONAL_ACCESS_TOKEN = settings.personal_access_token
REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_USERNAME = settings.redis_username
REDIS_PASSWORD = settings.redis_password
CACHE_TTL = settings.cache_ttl

redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    decode_responses=True,
    username=REDIS_USERNAME, 
    password=REDIS_PASSWORD
)

@app.get("/api/repos/{username}/")
def analyse_profile(username: str, page: int = 1):
    cache_key = make_cache_key(username, page)
    cached_repos = redis_client.get(cache_key)
    if cached_repos:
        return {"success": True, "repositories": json.loads(cached_repos)} # type: ignore
    
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

    redis_client.setex(cache_key, CACHE_TTL, json.dumps(repos_response))

    return {"success": True, "repositories": repos_response}
