# =============================================================================
# SOVEREIGN HARDENED APACHE DRUID
# Generated from template - Version: 29.0.1
# Constraint: debian-slim - Java runtime required
# Priority: scratch > distroless > wolfi > debian-slim (last resort)
# =============================================================================

ARG VERSION=29.0.1
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://dlcdn.apache.org/druid/${VERSION}/apache-druid-${VERSION}-bin.tar.gz" \
    -o /druid.tar.gz \
    && echo "PENDING  /druid.tar.gz" | sha256sum -c - \
    && tar -xzf /druid.tar.gz -C /opt \
    && rm /druid.tar.gz

FROM cgr.dev/chainguard/wolfi-base:latest

ARG VERSION
RUN apk add --no-cache ca-certificates python3
RUN useradd -m -u 65532 -s /usr/sbin/nologin druid 2>/dev/null || true
RUN mkdir -p /var/lib/druid /var/log/druid /var/cache/druid
COPY --from=builder /opt/apache-druid-${VERSION} /opt/druid
RUN chown -R druid:druid /opt/druid /var/lib/druid /var/log/druid /var/cache/druid
USER 65532:65532
WORKDIR /opt/druid
EXPOSE 8088 8888 8280
ENTRYPOINT ["/opt/druid/bin/start-druid"]
LABEL org.opencontainers.image.title="druid" \
      org.opencontainers.image.version="29.0.1" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.description="Sovereign hardened Apache Druid - real-time analytics database" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM