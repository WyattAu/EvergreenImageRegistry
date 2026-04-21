# =============================================================================
# SOVEREIGN HARDENED LANCEDB
# Generated from template - Version: 0.28.0-beta.9
# Constraint: debian-slim - no prebuilt binaries; built from source
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
#
# NOTE: LanceDB does not provide prebuilt binary releases.
# Built from source using Rust/Cargo.
# =============================================================================

ARG VERSION=0.28.0-beta.9
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates pkg-config libssl-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"
RUN git clone --depth 1 --branch v${VERSION} https://github.com/lancedb/lancedb.git /tmp/lancedb && \
    cd /tmp/lancedb && cargo build --release --bin lancedb && \
    cp target/release/lancedb /lancedb && rm -rf /tmp/lancedb

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libssl3 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' lancedb 2>/dev/null || true
RUN mkdir -p /app /var/log/lancedb /var/cache/lancedb && chown -R lancedb:lancedb /app /var/log/lancedb /var/cache/lancedb 2>/dev/null || true
COPY --from=builder /lancedb /usr/local/bin/lancedb
USER lancedb
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/lancedb", "--version"]
ENTRYPOINT ["/usr/local/bin/lancedb"]
LABEL org.opencontainers.image.title="lancedb" \
      org.opencontainers.image.version="0.28.0-beta.9" \
      org.opencontainers.image.vendor="LanceDB" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
