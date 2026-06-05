# =============================================================================
# EVERGREEN HARDENED EJDB
# Constraint: debian-slim - compile from source (C library)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=2.2.3
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532

# hadolint ignore=DL3023

ARG SHIM_VERSION=v0.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=2.2.3
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    build-essential cmake curl ca-certificates git && rm -rf /var/lib/apt/lists/* && \
    git clone --branch v${VERSION} https://github.com/Softmotions/ejdb.git /tmp/ejdb-src  || echo "Source repo not available - using binary not available - download failed" >&2 \
    exit 1" ; cd /tmp/ejdb-src ; mkdir build && cd build ; cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/ejdb ; make -j"$(nproc)" ; make install ; strip --strip-all /opt/ejdb/bin/ejdb 2>/dev/null 2>/dev/null ; \
    cd /tmp/ejdb-src ; mkdir build && cd build ; cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/ejdb ; make -j"$(nproc)" ; make install ; strip --strip-all /opt/ejdb/bin/ejdb 2>/dev/null 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=2.2.3
RUN apk add --no-cache libstdc++ ca-certificates \
    adduser -D -u 65532 -s /bin/false ejdb 2>/dev/null || true && \
    mkdir -p /var/lib/ejdb /var/log/ejdb /var/cache/ejdb 2>/dev/null || true
RUN mkdir -p /opt/ejdb || true
COPY --from=builder /opt/ejdb /opt/ejdb
RUN chown -R 65532:65532 /opt/ejdb /var/lib/ejdb /var/log/ejdb /var/cache/ejdb
USER 65532:65532
WORKDIR /var/lib/ejdb
EXPOSE 9191

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:9191"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="ejdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened EJDB - embedded JSON database engine" \
      org.opencontainers.image.vendor="Softmotions" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/Softmotions/ejdb.git"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
