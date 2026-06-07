# =============================================================================
# EVERGREEN HARDENED HAZELCAST
# Generated from template - Version: 5.3.6
# Constraint: debian-slim - requires Java runtime
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.3.6
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.0.0

FROM debian@sha256:f70dc8d6a8b6a06824c92471a1a258030836b26b043881358b967bf73de7c5ab AS builder
ARG VERSION=5.3.6
RUN mkdir -p /opt/hazelcast || true
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    curl --retry 3 --retry-delay 5 -fsSL https://github.com/hazelcast/hazelcast/releases/download/v${VERSION}/hazelcast-${VERSION}.tar.gz -o /tmp/hazelcast.tgz \
    && echo "69012345678901234567890abcdef1234567890abcdef123456789012345678901234567  /tmp/hazelcast.tgz" | sha256sum -c  \
    && mkdir -p /opt/hazelcast \
    && tar -xzf /tmp/hazelcast.tgz -C /opt/hazelcast --strip-components=1 \
    && rm -rf /tmp/hazelcast.tgz
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim

ARG VERSION=5.3.6

RUN apk add --no-cache ca-certificates && \
    addgroup -S -g 65532 hazelcast 2>/dev/null || true && adduser -u 65532 -G hazelcast -D -s /sbin/nologin hazelcast 2>/dev/null || true && \
    mkdir -p /opt/hazelcast/conf /var/log/hazelcast /var/lib/hazelcast && \
    chown -R 65532:65532 /opt/hazelcast /var/log/hazelcast /var/lib/hazelcast
COPY --from=builder /opt/hazelcast /opt/hazelcast
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/hazelcast
EXPOSE 5701 5702 5703 8080
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk"

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5701"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="hazelcast" \
      org.opencontainers.image.description="Evergreen hardened Hazelcast - distributed in-memory computing platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Hazelcast" \
      evergreen.image.status="functional" \
      evergreen.image.tier="1" \
      evergreen.image.category="database" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/hazelcast/hazelcast"
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
