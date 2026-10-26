# Render deployment

The repository includes a Render Blueprint at [`render.yaml`](../render.yaml). It defines:

- `vidbook-api`: the FastAPI service, backed by a 10 GB persistent disk at `/data`.
- `vidbook-frontend`: the Nginx-served React application, proxying `/api/` to the API service over Render's private network. The API host and port are injected from the Blueprint so Render's dynamic internal hostname is handled automatically.

The API uses SQLite and stores project files on the persistent disk. A persistent disk is intentional here: Render services otherwise have ephemeral filesystems. Render requires a paid service for persistent disks, so the API plan in the Blueprint is `0.5c-512mb`; the frontend remains on the free plan.

## Deploy

1. Push this repository to GitHub.
2. In the Render Dashboard, choose **New → Blueprint** and connect the GitHub repository.
3. Select the branch containing `render.yaml` and deploy the Blueprint.
4. When Render asks for `VIDBOOK_CORS_ORIGINS`, enter the public frontend URL, for example `https://vidbook-frontend.onrender.com`.
5. After both services are live, open the frontend service URL. The API health endpoint is available through the frontend at `/health`.

The generated `VIDBOOK_API_TOKEN` must remain secret. Do not commit Render environment values or a database file.

## Deploy behavior

The production services in `render.yaml` have auto-deploy disabled. The development services in `render.dev.yaml` also have auto-deploy disabled so that GitHub Actions is the single CD controller. The `deploy-dev.yml` workflow runs CI on every push to `develop`, then triggers the two development Render deploy hooks. The `deploy-production.yml` workflow is manual and uses the protected `production` GitHub environment before triggering the production hooks. Render's health check path is `/health`; failed deploys leave the previous healthy service in place. The `rollback.yml` workflow is also production-protected and redeploys both services from a specified known-good Git commit using Render deploy hooks.

## Important limitation

SQLite and a local project-file disk are suitable for this single-user deployment. The API must remain at one instance while using the disk. A future multi-instance deployment should migrate the database to Render Postgres and file storage to an object store.
