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
    python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir dnsvalidator==${VERSION} 2>/dev/null || \
    /opt/venv/bin/pip install --no-cache-dir dnsvalidator

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 libpython3.11 ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin dnsval 2>/dev/null || true
RUN mkdir -p /var/lib/dnsvalidator /var/log/dnsvalidator
COPY --from=builder /opt/venv /opt/venv
RUN chown -R 65534:65534 /opt/venv /var/lib/dnsvalidator /var/log/dnsvalidator
USER 65534:65534
WORKDIR /var/lib/dnsvalidator
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/opt/venv/bin/python3", "-c", "import dnsvalidator; print('ok')"]
ENTRYPOINT ["/opt/venv/bin/dnsvalidator"]
LABEL org.opencontainers.image.title="dnsvalidator" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened DNSValidator - DNS validation and testing tool" \
      sovereign.image.tier="1" \
      sovereign.image.category="security" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
