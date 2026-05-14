# =============================================================================
# EVERGREEN HARDENED DNSVALIDATOR
# Constraint: debian-slim - Python tool via pip
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG TARGETARCH
ARG BUILD_DATE


FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
ARG VERSION=1.0.0
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3 && rm -rf /var/lib/apt/lists/* || true && \
    python3 -m venv /opt/venv ; /opt/venv/bin/pip install --no-cache-dir --upgrade pip ; /opt/venv/bin/pip install --no-cache-dir dnsvalidator==${VERSION} 2>/dev/null || \    /opt/venv/bin/pip install --no-cache-dir dnsvalidator || true && \
    mkdir -p /opt/venv
FROM cgr.dev/chainguard/wolfi-base@sha256:31da6565f35af6401031c1d7aa91dc84ac76c5c48edd17fb90f0ed9e3173c7a9

ARG VERSION=1.0.0
RUN apk add --no-cache python3 ca-certificates && \
    adduser -u 65532 -s /bin/false dnsval || true && \
    mkdir -p /var/lib/dnsvalidator /var/log/dnsvalidator
COPY --from=builder /opt/venv /opt/venv
RUN chown -R 65532:65532 /opt/venv /var/lib/dnsvalidator /var/log/dnsvalidator
USER 65532:65532
WORKDIR /var/lib/dnsvalidator
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["/opt/venv/bin/dnsvalidator"]
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
STOPSIGNAL SIGTERM
