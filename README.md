# AI Agents Basics: Frontend + Tutorial API Run Guide

This repository includes:
- `tutorial-client`: Astro frontend
- `tutorial-api`: Flask API that discovers and runs lab tasks
- Lab folders (`1-ai-api-call` through `7-mcp`) used by the API

## Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Docker + Docker Compose (optional, recommended for API)

## 1) Run the Frontend (Astro)

From repository root:

```bash
cd tutorial-client
npm install
npm run dev
```

Frontend URL:
- `http://localhost:4321`

The frontend expects the API base URL from `PUBLIC_API_BASE`.
Default in development should be:
- `http://localhost:5050`

If needed, set it in `tutorial-client/.env`:

```bash
PUBLIC_API_BASE=http://localhost:5050
```

## 2) Run Tutorial API + Labs with Docker (Recommended)

From repository root.

Ensure root `.env` contains at least:
- `OPENAI_API_KEY`
- `OPENAI_API_BASE`
- `OPENAI_MODEL`

Single minimal image (API + labs + shared runtime deps):

```bash
docker compose -f tutorial-api/docker-compose.yml up --build
```

API URL:
- `http://localhost:5050`

### Detached mode

```bash
docker compose -f tutorial-api/docker-compose.yml up --build -d
```

### Stop

```bash
docker compose -f tutorial-api/docker-compose.yml down
```

### Run a lab Python file in the same container

```bash
docker compose -f tutorial-api/docker-compose.yml exec tutorial-api sh -c 'cd /app/1-ai-api-call && /opt/venv/bin/python task_1_import_setup.py'
```

## 3) Run API Locally (Alternative to Docker)

```bash
cd tutorial-api
pip install -r requirements.txt
python app.py
```

Local API URL:
- `http://localhost:5050`

## 4) Typical Full Workflow

1. Start API:

```bash
docker compose -f tutorial-api/docker-compose.yml up --build
```

2. In another terminal, start frontend:

```bash
cd tutorial-client
npm install
npm run dev
```

3. Open:
- Frontend: `http://localhost:4321`
- API health: `http://localhost:5050/api/health`

## Troubleshooting

- If frontend cannot reach API, verify `PUBLIC_API_BASE` points to the running API.
- If ports are busy, stop old containers/processes and retry.
- Rebuild after dependency changes: `docker compose -f tutorial-api/docker-compose.yml up --build`.
