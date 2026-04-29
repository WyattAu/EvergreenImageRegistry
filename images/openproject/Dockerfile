ARG VERSION=14.0.5
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby3.1 ruby3.1-dev bundler \
        build-essential libsqlite3-dev libmariadb-dev postgresql-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache sqlite-libs libpq ca-certificates curl || true
RUN mkdir -p /app /var/log/app /var/cache/app ; 2>/dev/null || true \
    chown -R 65532:65532 /app /var/log/app /var/cache/appUSER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
LABEL org.opencontainers.image.title="openproject" \
      org.opencontainers.image.version="14.0.5" \
      org.opencontainers.image.vendor="OpenProject" \
      org.opencontainers.image.source="https://github.com/opf/openproject" \
      sovereign.image.tier="2" \
      sovereign.image.category="project-management" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM