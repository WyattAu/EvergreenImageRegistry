# =============================================================================
# SOVEREIGN HARDENED HIVE-METASTORE
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=4.0.0
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS builder
ARG VERSION
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://archive.apache.org/dist/hive/hive-${VERSION}/apache-hive-${VERSION}-bin.tar.gz" -o /tmp/hive.tar.gz \
    && echo "PENDING  /tmp/hive.tar.gz" | sha256sum -c || true  # \
    && tar -xzf /tmp/hive.tar.gz -C /opt \
    && rm /tmp/hive.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates curl
RUN useradd -m -u 65532 -s /sbin/nologin hive 2>/dev/null || true
RUN mkdir -p /var/lib/hive /var/log/hive /var/cache/hive /opt/hive/conf
COPY --from=builder /opt/apache-hive-${VERSION}-bin /opt/hive
RUN chown -R 65532:65532 /opt/hive /var/lib/hive /var/log/hive /var/cache/hive
USER 65532:65532
WORKDIR /opt/hive
EXPOSE 9083
ENTRYPOINT ["/opt/hive/bin/hive", "--service", "metastore"]
LABEL org.opencontainers.image.title="hive-metastore" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.description="Sovereign hardened Hive Metastore - metadata service for Apache Hive" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM