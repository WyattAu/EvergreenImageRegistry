FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 py3-pip python3 git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir searxng-meta
RUN mkdir -p /app/config /app/data

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007

RUN apk add --no-cache python3 ca-certificates tzdata
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
RUN useradd -r -u 65532 -g nogroup -d /app -s /sbin/nologin searxng 2>/dev/null || true && \
    chown -R 65532:65532 /app 2>/dev/null || true
USER 65532:65532
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
EXPOSE 8888
ENTRYPOINT ["searxng-meta"]
LABEL org.opencontainers.image.title="searxng-meta" \
      org.opencontainers.image.description="SearXNG - meta variant" \
      org.opencontainers.image.vendor="searxng" \
      org.opencontainers.image.source="https://github.com/searxng/searxng" \
      sovereign.image.tier="3" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM