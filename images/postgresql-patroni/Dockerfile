# =============================================================================
# EVERGREEN HARDENED POSTGRESQL PATRONI
# Generated from template - Version: 4.0.3
# Constraint: debian-slim - Python runtime requires glibc + pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.3
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION} AS builder
ARG GITHUB_TOKEN
ARG VERSION=4.0.3
ARG PYTHON_VERSION=3.12-slim
RUN pip install --no-cache-dir --prefix=/install patroni[postgresql]=="${VERSION}" && \
    pip install --no-cache-dir --prefix=/install psycopg2-binary==2.9.9 && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache libpq curl ca-certificates || true
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /bin/false patroni 2>/dev/null || true && \
    mkdir -p /app /var/log/patroni /var/cache/patroni ; \
    chown -R 65532:65532 /app /var/log/patroni /var/cache/patroni
USER 65532:65532
WORKDIR /app
EXPOSE 8008 5432
ENV PATRONI_RESTAPI_LISTEN="0.0.0.0:8008"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD pg_isready -h localhost -p 5432
ENTRYPOINT ["python3", "-m", "patroni"]
LABEL org.opencontainers.image.title="postgresql-patroni" \
      org.opencontainers.image.version="4.0.3" \
      org.opencontainers.image.description="Patroni - PostgreSQL High Availability with etcd/Consul/ZooKeeper" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/patroni/patroni" \
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
