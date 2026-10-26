# Development

## Local startup

1. Create a virtual environment and install `backend/requirements.txt`.
2. Start the API from `backend/` with `uvicorn app.main:app --reload --port 8000`.
3. Install frontend dependencies from `frontend/` with `npm install`.
4. Start the UI with `npm run dev`.
5. Open <http://localhost:5173>.

The API creates `data/vidbook.db` and a folder tree under `data/projects/` on first use. Copy `.env.example` to `.env` to configure paths or an API token. The token is optional for localhost development and should be set before remote access.

## Docker Compose

Run `docker compose up --build`, then open <http://localhost:5173>. The database and project files are stored in the named `vidbook-data` volume.

## Production deployment and rollback

The production stack uses immutable GHCR image tags from `docker-compose.prod.yml`. On the deployment host, copy `ops/.env.prod.example` to `.env.prod`, set the image namespace, API token, and public origin, then run `bash ops/deploy.sh .env.prod`. To restore a known-good release, run `bash ops/rollback.sh v0.1.0 .env.prod`; the rollback selects the immutable version without changing the database volume.

GitHub Actions runs CI on every change. Pushes to `develop` run CI and then deploy to the Render development services using `RENDER_DEV_API_DEPLOY_HOOK_URL` and `RENDER_DEV_FRONTEND_DEPLOY_HOOK_URL`. Production deployment is manual through `deploy-production.yml`, protected by the GitHub `production` environment, using `RENDER_PROD_API_DEPLOY_HOOK_URL` and `RENDER_PROD_FRONTEND_DEPLOY_HOOK_URL`. The protected `rollback.yml` workflow redeploys a specified known-good commit to both Render production services. The tag workflow publishes versioned API and frontend images to GHCR.

## Tests

Run backend unit and API integration tests with `.venv/bin/python -m pytest` from `backend/`. Run frontend component and API-client tests with `npm test` from `frontend/`; validate the production bundle with `npm run build`. CI runs all three checks.

## Current foundation

This implementation covers the Phase 1 foundation plus the first Phase 2 research/evidence slice: project CRUD, local project-folder creation, approval gates, book shortlist approval, source registration, claim-level evidence records, a React dashboard, SQLite persistence, health checks, Docker Compose, and CI checks. Research file ingestion, AI-assisted ranking, script generation, and production exports remain staged for later phases described in the root README.
