ARG VERSION=6.0.3
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby3.1 ruby3.1-dev bundler \
        build-base libsqlite3-dev libmariadb-dev postgresql-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/*

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache sqlite-libs libpq ca-certificates curl
RUN mkdir -p /app /var/log/app /var/cache/app \
    && chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 3000
ENTRYPOINT ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
LABEL org.opencontainers.image.title="redmine" \
      org.opencontainers.image.version="6.0.3" \
      org.opencontainers.image.vendor="Redmine" \
      org.opencontainers.image.source="https://github.com/redmine/redmine" \
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