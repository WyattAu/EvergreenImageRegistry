# =============================================================================
# SOVEREIGN HARDENED QUESTDB-PYTHON
# QuestDB Python client library
# Constraint: debian-slim + Python venv
# =============================================================================

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 py3-pip python3 ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir questdb psycopg2-binary
RUN mkdir -p /app

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache python3 ca-certificates tzdata libpq
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
ENV PATH="/opt/venv/bin:${PATH}"
RUN groupadd -g 65532 -r questdb 2>/dev/null || true && \
    useradd -r -u 65532 -g questdb -d /app -s /sbin/nologin questdb 2>/dev/null || true && \
    chown -R 65532:65532 /app
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="questdb-python" \
      org.opencontainers.image.description="Sovereign QuestDB Python client with psycopg2 wire protocol support" \
      org.opencontainers.image.vendor="QuestDB" \
      org.opencontainers.image.source="https://github.com/questdb/questdb-python" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="database" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
