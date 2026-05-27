ARG VERSION=6.0.3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        ruby3.1 ruby3.1-dev bundler \
        build-essential libsqlite3-dev libmariadb-dev postgresql-dev \
        ca-certificates curl git && \
    rm -rf /var/lib/apt/lists/* || true

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache sqlite-libs libpq ca-certificates curl && \
    mkdir -p /app /var/log/app /var/cache/app ; 2>/dev/null || true ; \
    chown -R 65532:65532 /app /var/log/app /var/cache/app
USER 65532:65532
WORKDIR /app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:3000/ || exit 1
ENTRYPOINT ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
LABEL org.opencontainers.image.title="redmine" \
      org.opencontainers.image.description="redmine container image" \
      org.opencontainers.image.version="6.0.3" \
      org.opencontainers.image.vendor="Redmine" \
      org.opencontainers.image.source="https://github.com/redmine/redmine" \
      evergreen.image.tier="2" \
      evergreen.image.category="project-management" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="10s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
