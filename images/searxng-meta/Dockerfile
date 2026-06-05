
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-pip python3 git ca-certificates ; rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv || true
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir searxng-meta && \
    mkdir -p /app/config /app/data 2>/dev/null || true && { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="wolfi-base for musl compatibility"

RUN apk add --no-cache python3 ca-certificates tzdata
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN addgroup -S -g 2 nogroup >/dev/null || true && \
    adduser -u 65532 -G nogroup -D -h /app -s /bin/false searxng 2>/dev/null || true && \
    chown -R 65532:65532 /app/ && { echo "Binary not available - download failed" >&2; exit 1; }
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8888

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8888"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="searxng-meta" \
      org.opencontainers.image.description="SearXNG - meta variant" \
      org.opencontainers.image.vendor="searxng" \
      org.opencontainers.image.source="https://github.com/searxng/searxng" \
      evergreen.image.tier="3" \
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
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
