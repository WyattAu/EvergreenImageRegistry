# =============================================================================
# SOVEREIGN BASE - MUSL
# Minimal musl-based scratch image for statically-linked binaries.
# Uses Alpine's musl libc for C/C++ static compilation targets.
# =============================================================================

FROM cgr.dev/chainguard/static:latest

RUN apk add --no-cache 2>/dev/null || true

LABEL org.opencontainers.image.title="musl" \
      org.opencontainers.image.description="Sovereign musl-based static base for C/C++ compilation targets" \
      sovereign.image.tier="3" \
      sovereign.image.status="reference" \
      sovereign.image.category="base" \
      sovereign.image.note="Musl libc base for static binary builds. Use for Rust/C++ static targets."

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM