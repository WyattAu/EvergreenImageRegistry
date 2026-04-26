# =============================================================================
# SOVEREIGN HARDENED RUST
# Generated from template - Version: 1.78.0
# Constraint: debian-slim hardened multi-stage
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.78.0
ARG BUILD_DATE


FROM debian:bookworm-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    rust cargo ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN useradd -m -u 65532 -s /usr/bin/false rust 2>/dev/null || true
RUN mkdir -p /app /var/log/rust /var/cache/rust


FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache rust cargo ca-certificates 
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder --chown=65532:65532 /app /app
COPY --from=builder --chown=65532:65532 /var/log/rust /var/log/rust
COPY --from=builder --chown=65532:65532 /var/cache/rust /var/cache/rust
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["rust"]
LABEL org.opencontainers.image.title="rust" \
      org.opencontainers.image.version="1.78.0" \
      org.opencontainers.image.vendor="Rust" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.hardened="true"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM