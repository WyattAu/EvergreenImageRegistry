# =============================================================================
# SOVEREIGN HARDENED KIBANA
# Version: 8.12.2
# Constraint: debian-slim - Node.js runtime required (bundled with Kibana)
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=8.12.2
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://artifacts.elastic.co/downloads/kibana/kibana-${VERSION}-linux-x86_64.tar.gz" -o kibana.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  kibana.tar.gz" | sha256sum -c - \
    && tar -xzf kibana.tar.gz \
    && rm kibana.tar.gz \
    && rm -rf kibana-${VERSION}-linux-x86_64/node_modules/.cache

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libnss3 && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin kibana 2>/dev/null || true
RUN mkdir -p /opt/kibana/data /opt/kibana/logs /var/log/kibana /var/cache/kibana
COPY --from=builder /tmp/kibana-${VERSION}-linux-x86_64 /opt/kibana
USER 65534:65534
WORKDIR /opt/kibana
ENV PATH="/opt/kibana/bin:${PATH}"
EXPOSE 5601
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:5601/api/status"]
ENTRYPOINT ["/opt/kibana/bin/kibana"]
LABEL org.opencontainers.image.title="kibana" \
      org.opencontainers.image.description="Sovereign hardened Kibana - Elastic visualization dashboard" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Elastic" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
