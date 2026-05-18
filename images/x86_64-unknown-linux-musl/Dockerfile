# =============================================================================
# EVERGREEN BASE - x86_64-unknown-linux-musl
# Rust static compilation target base image.
# Provides musl toolchain for cargo build --target x86_64-unknown-linux-musl.
# =============================================================================


ARG APP_UID=65532
ARG APP_GID=65532

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

RUN apk add --no-cache  gcc rust cargo 2>/dev/null || true

USER 65532:65532
ENV RUST_TARGET="x86_64-unknown-linux-musl"
ENV CARGO_TARGET_DIR="/build"

WORKDIR /build
LABEL org.opencontainers.image.title="x86_64-unknown-linux-musl" \
      org.opencontainers.image.description="Evergreen Rust static build base for x86_64-unknown-linux-musl target" \
      evergreen.image.tier="3" \
      evergreen.image.status="reference" \
      evergreen.image.category="base" \
      evergreen.image.note="Rust static compilation base. Use for cargo build --target x86_64-unknown-linux-musl." \
            org.opencontainers.image.source="https://github.com/WyattAu/EvergreenImageRegistry" \
                  org.opencontainers.image.version="unknown"

LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:9101/metrics || exit 1
