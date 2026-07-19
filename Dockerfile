FROM node:20-alpine AS frontend-builder

WORKDIR /build/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CONFIG_PATH=/app/config.yaml

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y nginx supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY deploy/nginx.conf /etc/nginx/conf.d/mediabridge.conf
COPY deploy/supervisord.conf /etc/supervisor/conf.d/mediabridge.conf
COPY --from=frontend-builder /build/frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n"]
