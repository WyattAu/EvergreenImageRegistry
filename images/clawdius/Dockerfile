# =============================================================================
# EVERGREEN HARDENED CLAWDIUS
# Source build - scratch final stage
# Multi-stage: Rust toolchain builder -> scratch + CA certs
# =============================================================================
ARG VERSION=1.0.0
ARG RUST_VERSION=1.92.0
ARG SHIM_VERSION=v1.0.0

# ---------------------------------------------------------------------------
# Stage 1: Build Clawdius from source
# Since Clawdius has OpenSSL deps, we build against glibc (not musl static)
# Final binary will be dynamically linked -- use wolfi-base as runtime
# ---------------------------------------------------------------------------
FROM cgr.dev/chainguard/wolfi-base AS builder
ARG VERSION
ARG RUST_VERSION

RUN apk add --no-cache \
    build-base \
    ca-certificates \
    cmake \
    curl \
    git \
    linux-headers \
    openssl-dev \
    pkgconf \
    protobuf-dev

# Install Rust via rustup (reliable across versions)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | \
    sh -s -- -y --default-toolchain "${RUST_VERSION}" --profile minimal && \
    rm -rf /root/.rustup/toolchains/*/share
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /src
ARG VERSION
RUN git clone --depth 1 --branch "v${VERSION}" \
    "https://github.com/WyattAu/clawdius.git" /src && \
    rm -rf /src/.git

RUN cargo build --release --bin clawdius && \
    strip --strip-all /src/target/release/clawdius 2>/dev/null; \
    mkdir -p /app/data /app/config /app/logs

# ---------------------------------------------------------------------------
# Stage 2: Health shim
# ---------------------------------------------------------------------------
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# ---------------------------------------------------------------------------
# Stage 3: wolfi-base runtime (glibc + OpenSSL needed for dynamic binary)
# ---------------------------------------------------------------------------
FROM cgr.dev/chainguard/wolfi-base AS runtime
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /src/target/release/clawdius /usr/local/bin/clawdius
COPY --from=builder /app /app
COPY shim.toml /etc/evergreen/shim.toml

RUN apk add --no-cache ca-certificates libssl3

USER 65532:65532
ENV CLAWDIUS_CONFIG="/app/config/config.toml" \
    CLAWDIUS_DATA_DIR="/app/data" \
    CLAWDIUS_LOG_DIR="/app/logs" \
    RUST_LOG="info" \
    SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 8080 9101

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "/usr/local/bin/clawdius"]
CMD ["--", "server", "--host", "0.0.0.0", "--port", "8080"]
LABEL org.opencontainers.image.title="clawdius" \
      org.opencontainers.image.description="AI coding assistant with formal verification and multi-provider LLM" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="WyattAu" \
      org.opencontainers.image.source="https://github.com/WyattAu/clawdius" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="false"
LABEL evergreen.base.image="wolfi" \
      evergreen.build.type="source-build" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="exec" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="false" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
