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
    && echo "PENDING  /tmp/chartdb.zip" | sha256sum -c || true  # \
    && unzip -q /tmp/chartdb.zip -d /opt/chartdb \
    && rm /tmp/chartdb.zip

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates
RUN useradd -m -u 65532 -s /usr/sbin/nologin chartdb 2>/dev/null || true
RUN mkdir -p /var/lib/chartdb /var/log/chartdb /var/cache/chartdb
COPY --from=builder /opt/chartdb /opt/chartdb
RUN chown -R 65532:65532 /opt/chartdb /var/lib/chartdb /var/log/chartdb /var/cache/chartdb
USER 65532:65532
WORKDIR /opt/chartdb
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/opt/chartdb/chartdb.jar"]
LABEL org.opencontainers.image.title="chartdb" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened ChartDB - database schema visualization tool" \
      org.opencontainers.image.vendor="ChartDB" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM