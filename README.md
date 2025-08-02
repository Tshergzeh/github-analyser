# GitHub Analyser

## Description
APIs that take in a GitHub username and analyses the user's profile. The analysis returns the user's repositories, each with their number of stars, number of forks, languages used, and activity score. Activity score is calculated with this `(number_of_commits * 0.5) + (number_of_pull_requests * 0.3) + (number_of_issues * 0.1) + (number_of_stars * 0.1)`. Responses are stored in Redis cache and retrieved from the cache for 10 minutes after storage. Responses are paginated (default is 30 repos per page). This behaviour can be modified by setting the parameters. See Endpoints below.

## Features
- Analysis logic
- Caching
- Clean error handling

## Tech Stack
Python, FastAPI, Redis.

## Getting Started
1. Clone the repo  
2. Create virtual env  
3. `pip install -r requirements.txt`  
4. `uvicorn app.main:app --reload`

## Endpoint
- `GET /api/repos/{OWNER}?per_page=10&page=4`

## License
MIT
