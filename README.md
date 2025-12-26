# RemoteJob Radar

A lightweight job aggregator + matcher for remote roles.  
It ingests job posts from RSS feeds into Postgres and scores them against your profiles (keywords + exclusions).
![img.png](assets/full_frontend.png)
## Features
- **RSS ingest**: fetch jobs from multiple RSS sources and store them in Postgres
- **Dedup**: avoids saving duplicate jobs
- **Profiles**: create profiles with preferred keywords and excluded terms
- **Matching**: returns ranked job matches for a given profile
- **Simple UI**: minimal frontend served by FastAPI (optional)

---

## Tech Stack
- **Backend**: FastAPI, Uvicorn
- **DB**: PostgreSQL (Docker)
- **ORM**: SQLAlchemy
- **RSS parsing**: feedparser
- **Config**: pydantic-settings

---

## Requirements
- Python 3.11+ (recommended)
- Docker Desktop
- Git

---

## Setup

### 1) Create a virtual environment
```bash
python -m venv .venv
```

#### Activate:
Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2) Install Dependencies
```bash
pip install -r requirements.txt
```

### 3) Start Postgres (Docker)
```bash 
docker compose up -d
```
#### Check
```bash 
docker compose up -d
```

### 4) Create `.env` 
Create a `.env` file at project root:
```ini
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/radar
```


## Run the API 
```bash
python -m uvicorn app.main:app --reload 
# You can also use uvicorn directly: uvicorn app.main:app --reload
```
Open:
- API docs (Swagger UI): http://localhost:8000/docs
- Health: http://localhost:8000/health

## Usage

### 1) Ingest Jobs
Just click the button in the UI:  
![img.png](assets/ingest_jobs_frontend.png)

### 2) List Jobs
The jobs will appear in the UI:  
![img.png](assets/list_jobs_frontend.png)

### 3) Create a Profile
You can create profiles from the UI:   
![img.png](assets/create_profile_frontend.png)

### 4) Get matches for a profile
You can get matches for a profile from the UI:  
![img.png](assets/matches_frontend.png)

## Usage (Only Backend) 
### 1) Ingest Jobs
This will fetch jobs from configured RSS sources and save them into the DB:
```bash 
curl -X POST http://localhost:8000/ingest
```

### 2) List Jobs
```bash
curl "http://localhost:8000/jobs?limit=50"
```

### 3) Create a Profile
```bash 
curl -X POST http://127.0.0.1:8000/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example",
    "role_focus": "backend_mobile",
    "english_level": "B2",
    "keywords": ["python","fastapi","postgres","docker","aws","kotlin","laravel","api","integration"],
    "exclude_keywords": ["frontend","react","onsite","relocation"]
  }'
```
### 4) Get matches for a profile
```bash
curl "http://localhost:8000/profiles/1/matches?min_score=30&limit=30"
```
---
## Configure RSS Sources
RSS sources are defined in your settings (`app/core/config.py`)
Add more feeds to increase job volume and variety (remote tech boards, backend categories, etc.).
---
## Troubleshooting
### Postgres container is running but API can't connect?
Check:
1. Docker container is up: `docker compose ps`
2. Port 5432 is not used by another service: `netstat -an | grep 5432`
3. `.env` contains the correct DB URL
### "uvicorn not recognized"  
Use: 
`python -m uvicorn app.main:app --reload`  
and make sure you activated the venv.
---
## Roadmap
- CRUD for RSS sources
- Better normalization (company/location extraction)
- Scheduled ingest (cron / APScheduler)
- Full-text search + filters (remote-only, timezone, contract type
- Saved searches + email notifications)