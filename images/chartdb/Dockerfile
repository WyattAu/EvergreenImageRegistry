# =============================================================================
# SOVEREIGN HARDENED CHARTDB
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=1.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/chart-db/chartdb/releases/download/v${VERSION}/chartdb-${VERSION}.zip" -o /tmp/chartdb.zip \
    && echo "PENDING  /tmp/chartdb.zip" | sha256sum -c - \
    && unzip -q /tmp/chartdb.zip -d /opt/chartdb \
    && rm /tmp/chartdb.zip

FROM debian:bookworm-slim
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 65534 -s /usr/sbin/nologin chartdb 2>/dev/null || true
RUN mkdir -p /var/lib/chartdb /var/log/chartdb /var/cache/chartdb
COPY --from=builder /opt/chartdb /opt/chartdb
RUN chown -R 65534:65534 /opt/chartdb /var/lib/chartdb /var/log/chartdb /var/cache/chartdb
USER 65534:65534
WORKDIR /opt/chartdb
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8080"]
ENTRYPOINT ["java", "-jar", "/opt/chartdb/chartdb.jar"]
LABEL org.opencontainers.image.title="chartdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ChartDB - database schema visualization tool" \
      org.opencontainers.image.vendor="ChartDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
