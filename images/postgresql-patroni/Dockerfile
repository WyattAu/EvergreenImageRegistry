# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL PATRONI
# Generated from template - Version: 4.0.3
# Constraint: debian-slim - Python runtime requires glibc + pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.3
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12-slim



RUN mkdir -p /install 2>/dev/null || true
FROM python:${PYTHON_VERSION} AS builder
ARG VERSION=4.0.3
ARG PYTHON_VERSION=3.12-slim
RUN pip install --no-cache-dir --prefix=/install patroni[postgresql]=="${VERSION}" && \
    pip install --no-cache-dir --prefix=/install psycopg2-binary && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache libpq curl ca-certificates
COPY --from=builder /install /usr/local
RUN adduser -u 65532 -s /sbin/nologin patroni 2>/dev/null || true && \
    mkdir -p /app /var/log/patroni /var/cache/patroni && \
    chown -R 65532:65532 /app /var/log/patroni /var/cache/patroni
USER 65532:65532
WORKDIR /app
EXPOSE 8008 5432
ENV PATRONI_RESTAPI_LISTEN="0.0.0.0:8008"
ENTRYPOINT ["python3", "-m", "patroni"]
LABEL org.opencontainers.image.title="postgresql-patroni" \
      org.opencontainers.image.version="4.0.3" \
      org.opencontainers.image.description="Patroni - PostgreSQL High Availability with etcd/Consul/ZooKeeper" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/patroni/patroni" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM