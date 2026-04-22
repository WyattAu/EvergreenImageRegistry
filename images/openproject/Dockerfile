ARG VERSION=14.0.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby3.1 ruby3.1-dev bundler \
        build-essential libsqlite3-dev libmariadb-dev libpq-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby3.1 libsqlite3-0 libmariadb3 libpq5 \
        ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65534:65534 /app /var/log/app /var/cache/app
USER 65534:65534
WORKDIR /app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:3000"]
ENTRYPOINT ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
LABEL org.opencontainers.image.title="openproject" \
      org.opencontainers.image.version="14.0.5" \
      org.opencontainers.image.vendor="OpenProject" \
      org.opencontainers.image.source="https://github.com/opf/openproject" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
