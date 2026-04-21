# =============================================================================
# SOVEREIGN HARDENED VAULTWARDEN
# Generated from template - Version: 1.35.7
# Constraint: debian-slim - no prebuilt binaries; built from source
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
#
# NOTE: Vaultwarden does not provide prebuilt binary releases in GitHub.
# Built from source using Rust/Cargo. Web vault assets from bw_web_builds.
# =============================================================================

ARG VERSION=1.35.7
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates pkg-config libssl-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"
RUN git clone --depth 1 --branch ${VERSION} https://github.com/dani-garcia/vaultwarden.git /tmp/vaultwarden && \
    cd /tmp/vaultwarden && cargo build --release && \
    cp target/release/vaultwarden /vaultwarden && rm -rf /tmp/vaultwarden

FROM debian:bookworm-slim AS runner
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates libssl3 curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -g '' vaultwarden 2>/dev/null || true
RUN mkdir -p /app /var/log/vaultwarden /var/cache/vaultwarden && \
    chown -R vaultwarden:vaultwarden /app /var/log/vaultwarden /var/cache/vaultwarden 2>/dev/null || true
COPY --from=builder /vaultwarden /usr/local/bin/vaultwarden
USER vaultwarden
WORKDIR /app
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD vaultwarden --version
ENTRYPOINT ["vaultwarden"]
LABEL org.opencontainers.image.title="vaultwarden" \
      org.opencontainers.image.version="1.35.7" \
      org.opencontainers.image.vendor="Vaultwarden" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
