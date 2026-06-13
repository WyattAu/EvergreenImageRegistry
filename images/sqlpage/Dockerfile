ARG SHIM_VERSION=v1.1.0

FROM rust:1-slim AS builder
ARG VERSION=0.43.0
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc musl-tools && rm -rf /var/lib/apt/lists/* && \
    rustup target add x86_64-unknown-linux-musl && \
    RUSTFLAGS="-C target-feature=+crt-static" \
    cargo install --target x86_64-unknown-linux-musl --version ${VERSION} sqlpage

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /root/.cargo/bin/sqlpage /sqlpage
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="sqlpage" \
      org.opencontainers.image.description="SQL-only web application framework" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/sqlpage/SQLPage" \
      evergreen.image.tier="standard" \
      evergreen.image.category="web" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"
LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="prometheus"
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
