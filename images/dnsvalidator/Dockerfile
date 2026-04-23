# =============================================================================
# SOVEREIGN HARDENED DNSVALIDATOR
# Constraint: debian-slim - Python tool via pip
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3 && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir dnsvalidator==${VERSION} 2>/dev/null || \
    /opt/venv/bin/pip install --no-cache-dir dnsvalidator

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache python3 ca-certificates
RUN adduser -u 65532 -s /sbin/nologin dnsval 2>/dev/null || true
RUN mkdir -p /var/lib/dnsvalidator /var/log/dnsvalidator
COPY --from=builder /opt/venv /opt/venv
RUN chown -R 65532:65532 /opt/venv /var/lib/dnsvalidator /var/log/dnsvalidator
USER 65532:65532
WORKDIR /var/lib/dnsvalidator
EXPOSE 8080
ENTRYPOINT ["/opt/venv/bin/dnsvalidator"]
LABEL org.opencontainers.image.title="dnsvalidator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened DNSValidator - DNS validation and testing tool" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM