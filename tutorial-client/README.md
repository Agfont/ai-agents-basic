# Tutorial Frontend (Astro)

This UI maps each lab folder from the repository to a route and each task to one or more REST API calls served by the Flask backend.

## Routes

- `/` lists all lab directories discovered by the API.
- `/:lab/` shows task cards for a specific lab directory.
- `/:lab/tasks/:task/` shows task source, marker status, and run controls.

## REST calls used by the UI

- `GET /api/labs`
- `GET /api/labs/<lab_slug>`
- `GET /api/labs/<lab_slug>/tasks/<task_id>`
- `GET /api/labs/<lab_slug>/tasks/<task_id>/status`
- `POST /api/labs/<lab_slug>/tasks/<task_id>/run`

## Run locally

```bash
cd tutorial-client
cp .env.example .env
npm install
npm run dev
```

Default URL: `http://localhost:4321`
