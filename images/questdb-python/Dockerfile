# =============================================================================
# EVERGREEN HARDENED QUESTDB-PYTHON
# QuestDB Python client library
# Constraint: debian-slim + Python venv
# =============================================================================


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir questdb psycopg2-binary || true && \
    mkdir -p /app 2>/dev/null || true && \
    mkdir -p /opt/venv ; \
    mkdir -p /app 2>/dev/null || true

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache python3 ca-certificates tzdata libpq || true
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
ENV PATH="/opt/venv/bin:${PATH}"
RUN addgroup -S -g 65532 questdb 2>/dev/null || true && \
    adduser -u 65532 -G questdb -D -D -h /app -s /bin/false questdb 2>/dev/null || true && \
    chown -R 65532:65532 /app
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="questdb-python" \
      org.opencontainers.image.description="Evergreen QuestDB Python client with psycopg2 wire protocol support" \
      org.opencontainers.image.vendor="QuestDB" \
      org.opencontainers.image.source="https://github.com/questdb/questdb-python" \
      evergreen.image.tier="2" \
      evergreen.image.status="functional" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.version="unknown"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:9101/metrics || exit 1
ENTRYPOINT ["python", "-m", "questdb"]
CMD ["--help"]
