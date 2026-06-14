# =============================================================================
# EVERGREEN HARDENED REDIS
# Source build - scratch final stage
# =============================================================================
ARG VERSION=7.4.8
ARG SHIM_VERSION=v1.2.0

FROM cgr.dev/chainguard/wolfi-base AS builder
ARG VERSION
RUN apk add --no-cache gcc make glibc-dev linux-headers ca-certificates wget
WORKDIR /src
RUN wget -q "https://download.redis.io/releases/redis-${VERSION}.tar.gz" -O redis.tar.gz && \
    tar -xzf redis.tar.gz && rm redis.tar.gz
RUN cd redis-${VERSION} && \
    make -j$(nproc) MALLOC=libc BUILD_TLS=no LDFLAGS="-static" install && \
    mkdir -p /app /var/log/redis /var/cache/redis

FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=builder /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/redis /var/log/redis
COPY --from=builder /var/cache/redis /var/cache/redis
COPY shim.toml /etc/evergreen/shim.toml

USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /app
EXPOSE 6379 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "redis-server"]
CMD ["--", "--bind", "0.0.0.0", "--protected-mode", "no"]
LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.description="Redis - in-memory data structure store and cache (static build)" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      evergreen.image.tier="critical" \
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
