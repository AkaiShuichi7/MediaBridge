# MediaBridge Web

React, Vite, and TypeScript client for MediaBridge.

```bash
npm ci
npm run dev
```

The development server proxies `/api` to the FastAPI server on port 8000.
Production deployment is defined by the root-level monorepo infrastructure:
`../../infra/Dockerfile` and `../../infra/docker-compose.yml`.
