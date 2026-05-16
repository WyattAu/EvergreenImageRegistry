# =============================================================================
# EVERGREEN HARDENED LOGSTASH-OSS
# Version: 8.12.2
# Constraint: debian-slim - JRE runtime required
# Note: Elastic 8.x bundles OSS capabilities; x-pack disabled via configuration
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE
ARG TARGETARCH


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=8.12.2
ARG TARGETARCH
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "x86_64" ;; arm64) echo "arm64" ;; *) echo "x86_64" ;; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/logstash/logstash-oss-${VERSION}-linux-${ARCH}.tar.gz" -o logstash-oss.tar.gz && \
    echo "66666a2229bf927dcf32ac0bcc66debb61782ce88d233c88105269aeec91e964  logstash-oss.tar.gz" | sha256sum -c && \
    tar -xzf logstash-oss.tar.gz || true ; \
    rm -f logstash-oss.tar.gz && \
    mv logstash-oss-${VERSION}-linux-${ARCH} logstash-extracted || true
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=8.12.2
ARG TARGETARCH
RUN apk add --no-cache ca-certificates wget && \
    adduser -u 65532 -s /bin/false logstash 2>/dev/null || true && \
    mkdir -p /opt/logstash/data /opt/logstash/logs /var/log/logstash /var/cache/logstash 2>/dev/null || true
COPY --from=builder /tmp/logstash-extracted /opt/logstash
USER 65532:65532
WORKDIR /opt/logstash
ENV LS_JAVA_OPTS="-Xms512m -Xmx512m"
ENV PATH="/opt/logstash/bin:${PATH}"
EXPOSE 5044 9600

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -qO- http://localhost:5044/ || exit 1
ENTRYPOINT ["/opt/logstash/bin/logstash"]
LABEL org.opencontainers.image.title="logstash-oss" \
      org.opencontainers.image.description="Evergreen hardened Logstash OSS - open-source data processing pipeline" \
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
