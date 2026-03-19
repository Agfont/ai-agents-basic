# Tutorial API (Flask)

Minimal REST API for lab/tutorial orchestration.

This service is designed to run inside Docker using one shared Python environment (`/opt/venv`).

Environment variables are loaded at runtime from the repository root `.env` file via `docker-compose.yml` (`env_file: ../.env`).
Do not copy `.env` into the Docker image.

The Docker image is a single minimal runtime that includes:
- API code
- Lab source directories
- Shared Python dependencies required to run API and lab scripts

## Endpoints

- `GET /api/health`
- `GET /api/labs`
- `GET /api/labs/<lab_slug>`
- `GET /api/labs/<lab_slug>/tasks/<task_id>`
- `GET /api/labs/<lab_slug>/tasks/<task_id>/status`
- `POST /api/labs/<lab_slug>/tasks/<task_id>/run`
- `POST /api/labs/<lab_slug>/verify-environment`

The server auto-discovers repository directories that match `^\d+-` and task files that match `task_<n>_*.py`.

## Run locally

```bash
cd tutorial-api
pip install -r requirements.txt
python app.py
```

Default URL: `http://localhost:5050`

## Run with Docker (minimal runtime image)

Build and start:

```bash
docker compose -f tutorial-api/docker-compose.yml up --build
```

Run detached:

```bash
docker compose -f tutorial-api/docker-compose.yml up --build -d
```

Stop:

```bash
docker compose -f tutorial-api/docker-compose.yml down
```

## Run a lab Python file inside the same container

With the service running:

```bash
docker compose -f tutorial-api/docker-compose.yml exec tutorial-api sh -c 'cd /app/1-ai-api-call && /opt/venv/bin/python task_1_import_setup.py'
```

Or as a one-off command:

```bash
docker compose -f tutorial-api/docker-compose.yml run --rm tutorial-api sh -c 'cd /app/1-ai-api-call && /opt/venv/bin/python task_1_import_setup.py'
```

## Optimization notes

- Keep the virtual environment enabled in Docker: disabling it does not significantly reduce image size and loses isolation.
- Keep a single runtime target to reduce operational complexity and avoid split-image drift.
- Multi-stage build ensures only runtime executables and dependencies are present in final image.
