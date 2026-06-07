ARG SHIM_VERSION=v1.0.0

FROM rust:1-slim AS builder
ARG VERSION=1.17.1
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc musl-tools && rm -rf /var/lib/apt/lists/* && \
    rustup target add x86_64-unknown-linux-musl && \
    RUSTFLAGS="-C target-feature=+crt-static" \
    cargo install --target x86_64-unknown-linux-musl --version ${VERSION} qdrant

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /root/.cargo/bin/qdrant /qdrant
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 6333

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:6333"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="qdrant-cpu" \
      org.opencontainers.image.description="qdrant-cpu - vector similarity search engine (CPU-only)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="qdrant/qdrant" \
      org.opencontainers.image.source="https://github.com/qdrant/qdrant" \
      evergreen.image.tier="standard" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
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
