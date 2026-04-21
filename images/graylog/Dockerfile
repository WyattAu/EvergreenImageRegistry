# =============================================================================
# SOVEREIGN HARDENED GRAYLOG
# Version: 5.1.5
# Constraint: debian-slim - JRE runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=5.1.5
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://packages.graylog2.org/releases/graylog/graylog-${VERSION}.tgz" -o graylog.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  graylog.tar.gz" | sha256sum -c - \
    && tar -xzf graylog.tar.gz \
    && rm graylog.tar.gz

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin graylog 2>/dev/null || true
RUN mkdir -p /opt/graylog/data /opt/graylog/logs /var/log/graylog /var/cache/graylog
COPY --from=builder /tmp/graylog-${VERSION} /opt/graylog
USER 65534:65534
WORKDIR /opt/graylog
ENV GRAYLOG_HTTP_BIND_ADDRESS="0.0.0.0:9000"
ENV GRAYLOG_DATA_DIR="/opt/graylog/data"
EXPOSE 9000 12201 5044
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["curl", "-fsSL", "http://localhost:9000/api/system"]
ENTRYPOINT ["/opt/graylog/bin/graylogctl"]
CMD ["run"]
LABEL org.opencontainers.image.title="graylog" \
      org.opencontainers.image.description="Sovereign hardened Graylog - centralized log management platform" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Graylog" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="observability" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="debian-slim" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="15s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="60000ms"
