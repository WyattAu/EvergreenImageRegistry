# MIGRATION PLAN: python-alpine
# Current: FROM python:3.12-slim (Debian-based, banned per ADR-007)
# Target: FROM cgr.dev/chainguard/wolfi-base:latest
# Status: COMPLETE
# Note: Image name "python-alpine" is misleading — it was never Alpine-based.
#       It used python:3.12-slim which is Debian. Now uses wolfi (musl).
# Steps performed:
# 1. Replaced FROM python:3.12-slim with wolfi-base
# 2. Added: RUN apk add --no-cache python3 ca-certificates 
# 3. 
USER 65532:65532
# 4. Sovereign labels updated: sovereign.base.image="wolfi"
# ADR-008: Category D — migratable, no exception required

ARG VERSION=3.12
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
RUN apk add --no-cache python3 ca-certificates && \
    mkdir -p /app /var/log/python-alpine /var/cache/python-alpine ; \
    addgroup -g 65532 python && \
    adduser -u 65532 -G python -s /sbin/nologin -D python 
USER 65532:65532
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["python3"]
LABEL org.opencontainers.image.title="python-alpine" \
      org.opencontainers.image.version="3.12" \
      org.opencontainers.image.vendor="Python" \
      org.opencontainers.image.description="Sovereign hardened python-alpine - Python runtime on wolfi (musl)" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="10s"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
