# =============================================================================
# EVERGREEN HARDENED MEMCACHED
# Static build from source - scratch final stage
# =============================================================================
ARG VERSION=1.6.32
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532
ARG SHIM_VERSION=v1.0.0

FROM debian:bookworm-slim AS builder
ARG VERSION
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential linux-headers ca-certificates wget && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN wget -q "https://memcached.org/files/memcached-${VERSION}.tar.gz" -O memcached.tar.gz && \
    tar -xzf memcached.tar.gz && rm memcached.tar.gz
RUN cd memcached-${VERSION} && \
    ./configure \
        --prefix=/usr/local \
        --disable-dependency-tracking \
        --enable-static \
        --disable-shared && \
    make -j$(nproc) CFLAGS="-static -O2 -fstack-protector-strong" LDFLAGS="-static" && \
    make install

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /shim
COPY --from=builder /usr/local/bin/memcached /usr/local/bin/memcached
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

RUN ["/bin/sh", "-c", "mkdir -p /app /var/log/memcached /var/cache/memcached"]

USER ${APP_UID}:${APP_GID}
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 11211 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:11211"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="memcached" \
      org.opencontainers.image.description="Memcached - high-performance distributed memory caching system (static build)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Memcached" \
      org.opencontainers.image.source="https://github.com/memcached/memcached" \
      evergreen.image.tier="2" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true"
LABEL evergreen.base.image="scratch" \
      evergreen.build.type="musl-source" \
      evergreen.metrics.native="ztunnel" \
      evergreen.health.type="exec" \
      evergreen.security.cap-drop="ALL" \
      evergreen.security.no-new-privileges="true" \
      evergreen.security.read-only-rootfs="true" \
      evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
