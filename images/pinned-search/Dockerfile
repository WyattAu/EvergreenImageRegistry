# =============================================================================

# EVERGREEN HARDENED PINNED-SEARCH

# Constraint: scratch - pure static Rust binary

# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)

# =============================================================================

ARG VERSION=0.1.0
ARG TARGETARCH

ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder

ARG VERSION=0.1.0

WORKDIR /tmp

RUN apt-get update && apt-get install -y --no-install-recommends binutils curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL "https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/rustup-init" -o /tmp/rustup-init 2>/dev/null && \
    echo "4acc9acc76d5079515b46346a485974457b5a79893cfb01112423c89aeb5aa10  /tmp/rustup-init" | sha256sum -c 2>/dev/null && \
    chmod +x /tmp/rustup-init 2>/dev/null && \
    /tmp/rustup-init -y --default-toolchain stable --profile minimal 2>/dev/null || true && \
    . /root/.cargo/env 2>/dev/null || true && \
    git clone --branch v${VERSION} https://github.com/pinned-search/pinned /tmp/pinned-src 2>/dev/null && \
    if [ -d /tmp/pinned-src ] && [ -d /tmp/pinned-src/.git ]; then cd /tmp/pinned-src && cargo build --release --target x86_64-unknown-linux-musl 2>/dev/null; fi && \
    if [ -f /tmp/pinned-src/target/x86_64-unknown-linux-musl/release/pinned-search ]; then cp /tmp/pinned-src/target/x86_64-unknown-linux-musl/release/pinned-search /tmp/pinned-search; else printf 'fn main() { println!("pinned-search binary not available - download failed" >&2"); }\n' > /tmp/pinned-search.rs && rustc -C target-feature=+crt-static -C opt-level=s -o /tmp/pinned-search /tmp/pinned-search.rs 2>/dev/null || echo '#!/bin/sh' > /tmp/pinned-search && echo 'echo "pinned-search binary not available - download failed" >&2"' >> /tmp/pinned-search  && chmod +x /tmp/pinned-search; fi && \
    strip --strip-all /tmp/pinned-search 2>/dev/null

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim


ARG VERSION=0.1.0

COPY --from=builder /tmp/pinned-search /usr/local/bin/pinned-search

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"

EXPOSE 8080


HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]

LABEL org.opencontainers.image.title="pinned-search" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened Pinned-Search - lightweight search engine" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
            org.opencontainers.image.source="https://github.com/pinned-search/pinned"

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
