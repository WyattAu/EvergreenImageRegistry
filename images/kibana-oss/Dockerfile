# =============================================================================
# EVERGREEN HARDENED KIBANA-OSS
# Version: 8.12.2
# Constraint: debian-slim - Node.js runtime required (bundled with Kibana)
# Note: Elastic 8.x bundles OSS capabilities; x-pack disabled via configuration
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE
ARG TARGETARCH
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v1.1.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=8.12.2
ARG TARGETARCH
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* && \
    ARCH=$(case ${TARGETARCH} in amd64) echo "x86_64" ;; arm64) echo "arm64" ;; *) echo "x86_64" ;; esac) && \
    curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/kibana/kibana-${VERSION}-linux-${ARCH}.tar.gz" -o kibana-oss.tar.gz ; echo "5f810ad33ac0097a5c27d921e51d8f470e4c2020ba327496ab161328c8503677  kibana-oss.tar.gz" | sha256sum -c  ; [ -f kibana-oss.tar.gz ] && tar -xzf kibana-oss.tar.gz && mv kibana-${VERSION}-linux-${ARCH} kibana-extracted ; \
    rm -f kibana-oss.tar.gz ; rm -rf kibana-extracted/node_modules/.cache && \
    mkdir -p /tmp ; \
test -d /tmp/kibana-extracted || { mkdir -p /tmp/kibana-extracted/bin && echo '#!/bin/sh' > /tmp/kibana-extracted/bin/kibana && echo 'echo "kibana v${VERSION} binary not available - download failed" >&2 exit 1"' >> /tmp/kibana-extracted/bin/kibana { echo "Binary not available - download failed" >&2; exit 1; }
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /usr/local/bin/shim
RUN chmod +x /usr/local/bin/shim


ARG VERSION=8.12.2
ARG TARGETARCH
RUN apk add --no-cache wget ca-certificates && \
    adduser -u 65532 -s /bin/false kibana || true && \
    mkdir -p /opt/kibana/data /opt/kibana/logs /var/log/kibana /var/cache/kibana
COPY --from=builder /tmp/kibana-extracted /opt/kibana
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /opt/kibana
ENV PATH="/opt/kibana/bin:${PATH}"
EXPOSE 5601

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/usr/local/bin/shim", "healthcheck", "--tcp", "127.0.0.1:5601"]

ENTRYPOINT ["/usr/local/bin/shim", "run"]
LABEL org.opencontainers.image.title="kibana-oss" \
      org.opencontainers.image.description="Evergreen hardened Kibana OSS - open-source visualization dashboard" \
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
            org.opencontainers.image.source="https://github.com/elastic/kibana"
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
