# MediaBridge

MediaBridge is a single-repository product workspace for managing 115 offline
downloads and organizing media files. It contains the Web application today
and reserves clear homes for the browser extension and local Agent.

## Repository layout

```text
apps/
  server/       FastAPI service
  web/          React + Vite Web application
  extension/    Browser extension (reserved)
  agent/        Local MediaBridge Agent (reserved)
packages/
  api-contracts/ Shared API contract and generated clients (reserved)
infra/
  Dockerfile
  docker-compose.yml
  nginx/
  supervisor/
```

## Deploy

```bash
cp apps/server/config.example.yaml config.yaml
cp .env.example .env
mkdir -p db logs
# Edit config.yaml, then set a long MEDIABRIDGE_ADMIN_PASSWORD in .env.
docker compose -f infra/docker-compose.yml up -d
```

Open `http://<host>:8080` and sign in with the administrator credentials from
`.env`. When this port is behind an HTTPS reverse proxy, keep
`MEDIABRIDGE_COOKIE_SECURE=true`.

The FastAPI documentation endpoints are not exposed through the bundled Nginx
configuration. Do not add `/docs`, `/redoc`, or `/openapi.json` to a public
reverse proxy unless you explicitly need them.

## Authentication and future clients

The Web UI authenticates with an HttpOnly session cookie. API calls from the
future browser extension or Agent should instead use a personal access token:

```http
Authorization: Bearer mb_<token>
```

Create, list, and revoke tokens through `/api/auth/tokens`; a newly created
token is returned only once. This is the common authentication boundary for
all MediaBridge clients, independent of Emby users.

To use a different image name:

```bash
IMAGE_NAME=your-dockerhub-user/mediabridge:latest \
  docker compose -f infra/docker-compose.yml up -d
```

## Local development

```bash
cd apps/server
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn main:app --reload
```

In another terminal:

```bash
cd apps/web
npm ci
npm run dev
```

## Image publishing

The root Docker workflow builds the unified image only when `apps/server`,
`apps/web`, `infra`, or the workflow itself changes. Future extension and Agent
work can use their own workflows without rebuilding the main image.
