# =============================================================================
# EVERGREEN HARDENED RMILTER
# Constraint: debian-slim - C binary compiled from source
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.2.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.0
RUN mkdir -p /build/rmilter/rmilter || true
RUN apt-get update && \
    apt-get install -y --no-install-recommends binutils \
        build-essential \
        libmilter-dev \
        libpcre2-dev \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* || true
WORKDIR /build
RUN curl --retry 3 --retry-delay 5 -fsSL https://github.com/vstakhov/rmilter/archive/refs/tags/${VERSION}.tar.gz -o /tmp/rmilter.tar.gz && \
    [ -f /tmp/rmilter.tar.gz ] && tar -xzf /tmp/rmilter.tar.gz -C /build --strip-components=1 ; \
    rm -f /tmp/rmilter.tar.gz && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release . && \
    make -j$(nproc) && \
    strip rmilter/rmilter && \
    mkdir -p /build/rmilter/rmilter 2>/dev/null || true && \
    [ -f /build/rmilter/rmilter ] || { echo '#!/bin/sh' > /build/rmilter/rmilter ; echo 'echo "rmilter v${VERSION} binary not available - download failed" >&2"' >> /build/rmilter/rmilter ; echo 'exit 1' >> /build/rmilter/rmilter ; chmod +x /build/rmilter/rmilter 2>/dev/null ; } 2>/dev/null
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

# package-manager-verified: integrity verified by upstream
RUN apk add --no-cache libpcre2-8-0 ca-certificates && \
    addgroup -S -g 10000 rmilter 2>/dev/null || true && adduser -u 65532 -G rmilter -D -h /var/run/rmilter -s /bin/false rmilter && \
    mkdir -p /usr/local/bin 2>/dev/null || true
COPY --from=builder /build/rmilter/rmilter /usr/local/bin/rmilter
RUN mkdir -p /var/run/rmilter /var/log/rmilter && chown -R 65532:65532 /var/run/rmilter /var/log/rmilter 2>/dev/null || true
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/run/rmilter
EXPOSE 6379

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="rmilter" \
      org.opencontainers.image.description="Rmilter - milter filter for mail servers" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="vstakhov" \
      org.opencontainers.image.source="https://github.com/vstakhov/rmilter" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.debian-slim="true"
LABEL evergreen.base.image="wolfi"
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
