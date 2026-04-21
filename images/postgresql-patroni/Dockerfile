# =============================================================================
# SOVEREIGN HARDENED POSTGRESQL PATRONI
# Generated from template - Version: 4.0.3
# Constraint: debian-slim - Python runtime requires glibc + pip
# Priority: scratch > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=4.0.3
ARG BUILD_DATE
ARG PYTHON_VERSION=3.12-slim

FROM python:${PYTHON_VERSION} AS builder
RUN pip install --no-cache-dir --prefix=/install patroni[postgresql]=="${VERSION}" && \
    pip install --no-cache-dir --prefix=/install psycopg2-binary && \
    find /install -type f -name "*.pyc" -delete && \
    find /install -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip libpq5 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
COPY --from=builder /install /usr/local
RUN useradd -m -u 65534 -s /usr/sbin/nologin patroni 2>/dev/null || true && \
    mkdir -p /app /var/log/patroni /var/cache/patroni && \
    chown -R 65534:65534 /app /var/log/patroni /var/cache/patroni
USER 65534:65534
WORKDIR /app
EXPOSE 8008 5432
ENV PATRONI_RESTAPI_LISTEN="0.0.0.0:8008"
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python3", "-c", "import patroni; print('ok')"]
ENTRYPOINT ["python3", "-m", "patroni"]
LABEL org.opencontainers.image.title="postgresql-patroni" \
      org.opencontainers.image.version="4.0.3" \
      org.opencontainers.image.description="Patroni - PostgreSQL High Availability with etcd/Consul/ZooKeeper" \
      org.opencontainers.image.vendor="Zalando" \
      org.opencontainers.image.source="https://github.com/patroni/patroni" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
