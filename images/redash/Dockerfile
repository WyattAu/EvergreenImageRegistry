# =============================================================================

# EVERGREEN HARDENED REDASH

# Generated from template - Version: 10.0.0

# Constraint: debian-slim - Python runtime with web dependencies

# Priority: scratch > distroless > wolfi > debian-slim (fallback)

# =============================================================================

ARG VERSION=10.0.0
ARG TARGETARCH

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM python@sha256:46cb7cc2877e60fbd5e21a9ae6115c30ace7a077b9f8772da879e4590c18c2e3 AS builder

ARG VERSION=10.0.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential postgresql-dev curl && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --prefix=/install \
    redash=="${VERSION}" || true && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null  && \binary not available - download failed" >&2 exit 1"' >> /install && echo 'exit 1' >> /install && chmod +x /install ; }

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache libpq curl ca-certificates

COPY --from=builder /install /usr/local

RUN adduser -u 65532 -s /bin/false redash || true && \
    mkdir -p /app /var/log/redash /var/cache/redash ;  chown -R 65532:65532 /app /var/log/redash /var/cache/redash || true

USER 65532:65532

WORKDIR /app

EXPOSE 5000

ENV REDASH_WEB_WORKERS="4"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:5000/ || exit 1

ENTRYPOINT ["redash", "server"]

LABEL org.opencontainers.image.title="redash" \
      org.opencontainers.image.version="10.0.0" \
      org.opencontainers.image.description="Redash - Open Source Data Visualization and Dashboards" \
      org.opencontainers.image.vendor="Redash" \
      org.opencontainers.image.source="https://github.com/getredash/redash" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi"

LABEL evergreen.metrics.native="ztunnel"

LABEL evergreen.health.type="exec"

LABEL evergreen.security.cap-drop="ALL"

LABEL evergreen.security.no-new-privileges="true"

LABEL evergreen.security.read-only-rootfs="true"

LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101

STOPSIGNAL SIGTERM
