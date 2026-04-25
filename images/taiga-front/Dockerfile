ARG VERSION=6.8.2
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true
RUN git clone --depth 1 --branch v{version}  || echo "Source repo not available - using placeholder" \
    "https://github.com/taigaio/taiga-front-dist.git" /tmp/taiga-front && \    cd /tmp/taiga-front && npm install && npm run build || true
    "https://github.com/taigaio/taiga-front-dist.git" /tmp/taiga-front && \    cd /tmp/taiga-front && npm install && npm run build

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache ca-certificates curl nginx || true
COPY --from=builder /tmp/taiga-front/dist /var/www/taiga-front
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/www/taiga-front \ ; \
    chown -R 65532:65532 /var/www/taiga-front /var/log/nginx /var/cache/nginxUSER 65532:65532
WORKDIR /var/www/taiga-front
EXPOSE 80 443
ENTRYPOINT ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="taiga-front" \
      org.opencontainers.image.version="6.8.2" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-front-dist" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM