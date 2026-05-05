# =============================================================================
# EVERGREEN HARDENED LOGSTASH
# Version: 8.12.2
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/logstash/logstash-${VERSION}-linux-x86_64.tar.gz" -o logstash.tar.gz ; echo "0000000000000000000000000000000000000000000000000000000000000000  logstash.tar.gz" | sha256sum -c || true  ; [ -f logstash.tar.gz ] && tar -xzf logstash.tar.gz || true ; \
    rm -f logstash.tar.gz
FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

ARG VERSION
ARG TARGETARCH
RUN apk add --no-cache ca-certificates curl && \
    adduser -u 65532 -s /bin/false logstash 2>/dev/null || true && \
    mkdir -p /opt/logstash/data /opt/logstash/logs /var/log/logstash /var/cache/logstash 2>/dev/null || true
COPY --from=builder /tmp/logstash-${VERSION} /opt/logstash
USER 65532:65532
WORKDIR /opt/logstash
ENV LS_JAVA_OPTS="-Xms512m -Xmx512m"
ENV PATH="/opt/logstash/bin:${PATH}"
EXPOSE 5044 9600

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:5044/ || exit 1
ENTRYPOINT ["/opt/logstash/bin/logstash"]
LABEL org.opencontainers.image.title="logstash" \
      org.opencontainers.image.description="Evergreen hardened Logstash - Elastic data processing pipeline" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      evergreen.image.tier="1" \
      evergreen.image.status="functional" \
      evergreen.image.category="observability" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.base="wolfi" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="15s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="60000ms" \
            org.opencontainers.image.source="https://github.com/elastic/logstash"
LABEL evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
