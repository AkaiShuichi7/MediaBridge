FROM node:20-alpine AS frontend-builder

WORKDIR /build/apps/web

COPY apps/web/package*.json ./
RUN npm ci

COPY apps/web/ ./
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

COPY apps/server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/server/ ./
COPY infra/nginx/nginx.conf /etc/nginx/conf.d/mediabridge.conf
COPY infra/supervisor/supervisord.conf /etc/supervisor/conf.d/mediabridge.conf
COPY --from=frontend-builder /build/apps/web/dist /usr/share/nginx/html

EXPOSE 80

CMD ["/usr/bin/supervisord", "-n"]
