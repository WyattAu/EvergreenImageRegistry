ARG VERSION=3.12-slim
ARG BUILD_DATE

FROM python:3.12-slim AS builder
RUN mkdir -p /app /var/log/python-slim /var/cache/python-slim

FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
COPY --from=builder /var/log/python-slim /var/log/python-slim
COPY --from=builder /var/cache/python-slim /var/cache/python-slim
RUN useradd -r -u 65534 -g '' python 2>/dev/null || true
USER 65534:65534
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python3", "--version"]
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="python-slim" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.vendor="Python" \
      org.opencontainers.image.description="Sovereign hardened python-slim - minimal Python runtime" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
