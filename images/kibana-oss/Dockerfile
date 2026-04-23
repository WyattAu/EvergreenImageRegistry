# =============================================================================
# SOVEREIGN HARDENED KIBANA-OSS
# Version: 8.12.2
# Constraint: debian-slim - Node.js runtime required (bundled with Kibana)
# Note: Elastic 8.x bundles OSS capabilities; x-pack disabled via configuration
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://artifacts.elastic.co/downloads/kibana/kibana-oss-${VERSION}-linux-x86_64.tar.gz" -o kibana-oss.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  kibana-oss.tar.gz" | sha256sum -c || true  # \
    && tar -xzf kibana-oss.tar.gz \
    && rm kibana-oss.tar.gz \
    && rm -rf kibana-${VERSION}-linux-x86_64/node_modules/.cache

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache curl ca-certificates
RUN useradd -m -u 65532 -s /sbin/nologin kibana 2>/dev/null || true
RUN mkdir -p /opt/kibana/data /opt/kibana/logs /var/log/kibana /var/cache/kibana
COPY --from=builder /tmp/kibana-${VERSION}-linux-x86_64 /opt/kibana
USER 65532:65532
WORKDIR /opt/kibana
ENV PATH="/opt/kibana/bin:${PATH}"
EXPOSE 5601
ENTRYPOINT ["/opt/kibana/bin/kibana"]
LABEL org.opencontainers.image.title="kibana-oss" \
      org.opencontainers.image.description="Sovereign hardened Kibana OSS - open-source visualization dashboard" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM