ARG VERSION=6.8.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        nodejs npm ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 --branch v{version} \
    "https://github.com/taigaio/taiga-front-dist.git" /tmp/taiga-front && \
    cd /tmp/taiga-front && npm install && npm run build

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl nginx && \
    rm -rf /var/lib/apt/lists/*
COPY --from=builder /tmp/taiga-front/dist /var/www/taiga-front
RUN mkdir -p /var/log/nginx /var/cache/nginx /var/www/taiga-front \
    && chown -R 65534:65534 /var/www/taiga-front /var/log/nginx /var/cache/nginx
USER 65534:65534
WORKDIR /var/www/taiga-front
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-f", "http://localhost:80"]
ENTRYPOINT ["nginx", "-g", "daemon off;"]
LABEL org.opencontainers.image.title="taiga-front" \
      org.opencontainers.image.version="6.8.2" \
      org.opencontainers.image.vendor="Taiga" \
      org.opencontainers.image.source="https://github.com/taigaio/taiga-front-dist" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="30000ms"
