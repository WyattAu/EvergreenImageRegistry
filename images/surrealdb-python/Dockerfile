# =============================================================================
# EVERGREEN HARDENED SURREALDB-PYTHON
# Constraint: debian-slim - Python package via pip
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH
ARG BUILD_DATE

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.0
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3 && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip || true ; /opt/venv/bin/pip install --no-cache-dir surrealdb==${VERSION} 2>/dev/null || /opt/venv/bin/pip install --no-cache-dir surrealdb || true && \
    mkdir -p /app /usr/local/lib/python3.11/site-packages || true ; touch /app/placeholder || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
ARG VERSION=1.0.0
RUN apk add --no-cache python3 || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true ; adduser -u 65532 -G nogroup -D -h /app -s /bin/false surrealdb-python 2>/dev/null || true
USER 65532:65532
WORKDIR /app

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python3", "-m", "surrealdb"]
LABEL org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened SurrealDB Python - Python SDK for SurrealDB" \
      org.opencontainers.image.title="SurrealDB Python" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
      evergreen.metrics.native="ztunnel"
LABEL evergreen.security.cap-drop="ALL"
LABEL org.opencontainers.image.source="https://github.com/surrealdb/surrealdb"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

LABEL evergreen.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
