ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=0.21.0
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-${TARGETARCH}.tar.zst -o /ollama.tar.gz && \
    echo "a7fc4261298aeca8f785f695978a5e997004d414c13d4cfb965a10da9f4db6ea  /ollama.tar.gz" | sha256sum -c ; \
    [ -f /ollama.tar.gz ] && tar -xzf /ollama.tar.gz -C / && rm -f /ollama.tar.gz && chmod +x /ollama 2>/dev/null ; \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/ollama/ollama/releases/download/v0.21.0/ollama-linux-${TARGETARCH}.tar.zst -o /ollama && { echo "Binary not available - download failed" >&2; exit 1; }
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG TARGETARCH
RUN mkdir -p /app /var/log/ollama /var/cache/ollama 2>/dev/null || true


FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim

COPY --from=downloader /ollama /ollama
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/ollama /var/log/ollama
COPY --from=builder /var/cache/ollama /var/cache/ollama
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 11434

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:11434"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/ollama"]
LABEL org.opencontainers.image.title="ollama" \
      org.opencontainers.image.description="ollama container image" \
      org.opencontainers.image.version="0.21.0" \
      org.opencontainers.image.vendor="Ollama" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/ollama/ollama"

LABEL evergreen.base.image="scratch"
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
