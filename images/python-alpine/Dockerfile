ARG VERSION=3.12-slim
ARG BUILD_DATE

FROM python:3.12-slim AS builder
RUN mkdir -p /app /var/log/python-alpine /var/cache/python-alpine

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/python-alpine /var/log/python-alpine
COPY --from=builder /var/cache/python-alpine /var/cache/python-alpine
RUN useradd -r -u 65534 -g '' python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "--version"]
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="python-alpine" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.vendor="Python" \
      org.opencontainers.image.description="Sovereign hardened python-alpine - Python runtime (no Alpine, debian-slim)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
