ARG VERSION=8.0.2
ARG SHIM_VERSION=v2.0.0

# Build stage: compile Redis from source as static binary
FROM cgr.dev/chainguard/wolfi-base@sha256:a31344ab2cb8618db84f535eec56f76f6178b142cb92cb2e48676cc2dcebea72 AS builder
ARG VERSION
RUN apk add --no-cache gcc make glibc-dev linux-headers ca-certificates wget
WORKDIR /src
RUN wget -q "https://download.redis.io/releases/redis-${VERSION}.tar.gz" -O redis.tar.gz && \
    tar -xzf redis.tar.gz && rm redis.tar.gz
RUN cd redis-${VERSION} && \
    make -j$(nproc) MALLOC=libc BUILD_TLS=no LDFLAGS="-static" install

# Shim stage
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

# Final stage: scratch with only the binary + shim
FROM scratch
COPY --from=shim /shim /usr/local/bin/shim
COPY --from=builder /usr/local/bin/redis-server /usr/local/bin/redis-server
COPY --from=builder /usr/local/bin/redis-cli /usr/local/bin/redis-cli
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Non-root execution
RUN mkdir -p /data && chown -R 65532:65532 /data
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /data

EXPOSE 6380 9101

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:6379"]

ENTRYPOINT ["/usr/local/bin/shim", "run", "-c", "redis-server"]
CMD ["--dir", "/data", "--bind", "0.0.0.0", "--protected-mode", "no"]

LABEL org.opencontainers.image.title="redis" \
      org.opencontainers.image.description="Redis - source-built, static, non-root, distroless" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Redis" \
      org.opencontainers.image.source="https://github.com/redis/redis" \
      evergreen.image.tier="critical" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.distroless="true"
LABEL evergreen.base.image="scratch"
LABEL evergreen.build.type="musl-source"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"
LABEL prometheus.io/scrape="true" \
      prometheus.io/port="9101" \
      prometheus.io/path="/metrics"
STOPSIGNAL SIGTERM
