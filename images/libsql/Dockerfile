ARG SHIM_VERSION=v0.3.0

FROM rust:1-slim AS builder
ARG VERSION=0.24.32
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc musl-tools protobuf-compiler cmake clang git && rm -rf /var/lib/apt/lists/* && \
    rustup target add x86_64-unknown-linux-musl && \
    git clone --depth 1 --branch libsql-server-v${VERSION} https://github.com/tursodatabase/libsql.git /src
WORKDIR /src
RUN RUSTFLAGS="-C target-feature=+crt-static" \
    cargo build --release --target x86_64-unknown-linux-musl --bin libsql-server

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /src/target/x86_64-unknown-linux-musl/release/libsql-server /libsql-server
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/lib/libsql
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="libsql-server" \
      org.opencontainers.image.description="Turso libSQL server - open-source SQLite fork with networking" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/tursodatabase/libsql" \
      evergreen.image.tier="standard" \
      evergreen.image.category="database" \
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
