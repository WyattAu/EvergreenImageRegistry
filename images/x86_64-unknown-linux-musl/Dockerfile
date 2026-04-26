# =============================================================================
# SOVEREIGN BASE - x86_64-unknown-linux-musl
# Rust static compilation target base image.
# Provides musl toolchain for cargo build --target x86_64-unknown-linux-musl.
# =============================================================================


FROM cgr.dev/chainguard/static:latest

RUN apk add --no-cache  gcc rust cargo 2>/dev/null 

ENV RUST_TARGET="x86_64-unknown-linux-musl"
ENV CARGO_TARGET_DIR="/build"

WORKDIR /build
LABEL org.opencontainers.image.title="x86_64-unknown-linux-musl" \
      org.opencontainers.image.description="Sovereign Rust static build base for x86_64-unknown-linux-musl target" \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Rust static compilation base. Use for cargo build --target x86_64-unknown-linux-musl."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM