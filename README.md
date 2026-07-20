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
mkdir -p db logs
# Edit config.yaml and set the 115 cookies and library paths.
docker compose -f infra/docker-compose.yml up -d
```

Open `http://<host>:8080`. API documentation is available at
`http://<host>:8080/docs`.

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
