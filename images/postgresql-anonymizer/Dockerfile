# =============================================================================

# EVERGREEN HARDENED POSTGRESQL ANONYMIZER

# Generated from template - Version: 1.2.0

# Constraint: debian-slim - PostgreSQL dev libs + Python pip

# Priority: scratch > distroless > wolfi > debian-slim (fallback)

# =============================================================================

ARG VERSION=1.2.0
ARG TARGETARCH

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

FROM python@sha256:46cb7cc2877e60fbd5e21a9ae6115c30ace7a077b9f8772da879e4590c18c2e3 AS builder

ARG VERSION=1.2.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-server-dev-all postgresql-dev && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --prefix=/install \
    postgresql-anonymizer=="${VERSION}" || true && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null  && && { echo "Binary not available - download failed" >&2; exit 1; }

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache postgresql-client libpq curl ca-certificates

COPY --from=builder /install /usr/local

RUN adduser -u 65532 -s /bin/false anon || true && \
    mkdir -p /app /var/log/pg-anonymizer /var/cache/pg-anonymizer ;  chown -R 65532:65532 /app /var/log/pg-anonymizer /var/cache/pg-anonymizer

USER 65532:65532

WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1

ENTRYPOINT ["python3", "-m", "postgresql_anonymizer"]

LABEL org.opencontainers.image.title="postgresql-anonymizer" \
      org.opencontainers.image.version="1.2.0" \
      org.opencontainers.image.description="PostgreSQL Anonymizer - Data Anonymization Extension" \
      org.opencontainers.image.vendor="Dalibo" \
      org.opencontainers.image.source="https://github.com/Dalibo/postgresql_anonymizer" \
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
