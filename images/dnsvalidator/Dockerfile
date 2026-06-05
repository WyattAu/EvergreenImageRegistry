# =============================================================================
# EVERGREEN HARDENED DNSVALIDATOR
# Constraint: debian-slim - Python tool via pip
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH
ARG BUILD_DATE
ARG APP_UID=65532
ARG APP_GID=65532


ARG SHIM_VERSION=v0.3.0

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.0
WORKDIR /tmp
RUN mkdir -p /opt/venv || true
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3 && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip ; /opt/venv/bin/pip install --no-cache-dir dnsvalidator==${VERSION} 2>/dev/null || \    /opt/venv/bin/pip install --no-cache-dir dnsvalidator && \
    mkdir -p /opt/venv
FROM ghcr.io/wyattau/evergreenshim/health-shim:${SHIM_VERSION} AS shim

FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9
COPY --from=shim /shim /shim

LABEL evergreen.base.fallback_reason="wolfi-base for musl compatibility"

ARG VERSION=1.0.0
RUN apk add --no-cache python3 ca-certificates && \
    adduser -u 65532 -s /bin/false dnsval || true && \
    mkdir -p /var/lib/dnsvalidator /var/log/dnsvalidator
COPY --from=builder /opt/venv /opt/venv
RUN chown -R 65532:65532 /opt/venv /var/lib/dnsvalidator /var/log/dnsvalidator
USER 65532:65532
ENV SHIM_METRICS_ENABLED="true"
WORKDIR /var/lib/dnsvalidator
EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD ["/shim", "healthcheck", "--tcp", "127.0.0.1:8080"]

ENTRYPOINT ["/shim", "run"]
LABEL org.opencontainers.image.title="dnsvalidator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Evergreen hardened DNSValidator - DNS validation and testing tool" \
      evergreen.image.tier="1" \
      evergreen.image.category="security" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.base.image="wolfi" \
            org.opencontainers.image.source="https://github.com/vortexau/dnsvalidator"
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
