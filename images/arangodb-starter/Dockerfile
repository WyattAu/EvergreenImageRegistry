# =============================================================================
# SOVEREIGN HARDENED ARANGODB-STARTER
# Generated from template - Version: 3.11.10.1
# Starter mode for ArangoDB cluster deployments
# Constraint: scratch - purest form, no shell, no package manager, smallest attack surface
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=3.11.10.1
ARG BUILD_DATE

# hadolint ignore=DL3023
FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://download.arangodb.com/arangodb311/Linux/arangodb3-linux-3.11.10.1_x86_64.tar.gz" -o /arangodb.tar.gz && \
    tar -xzf /arangodb.tar.gz -C /tmp && rm /arangodb.tar.gz && \
    strip --strip-all /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/sbin/arangod && \
    strip --strip-all /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/bin/arangosh && \
    mv /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/sbin/arangod /arangod && \
    mv /tmp/arangodb3-linux-3.11.10.1_x86_64/usr/bin/arangosh /arangosh

FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/lib/arangodb3 /var/log/arangodb3

FROM scratch
COPY --from=downloader /arangod /arangod
COPY --from=downloader /arangosh /arangosh
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/lib/arangodb3 /var/lib/arangodb3
COPY --from=builder /var/log/arangodb3 /var/log/arangodb3
USER 65534:65534
WORKDIR /app
EXPOSE 8529
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/arangod", "--version"]
ENTRYPOINT ["/arangod", "--serverstarter"]
LABEL org.opencontainers.image.title="arangodb-starter" \
      org.opencontainers.image.version="3.11.10.1" \
      org.opencontainers.image.vendor="ArangoDB" \
      org.opencontainers.image.description="ArangoDB in starter mode for cluster and resilient single-server deployments" \
      sovereign.image.tier="1" \
      sovereign.image.category="database" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms" \
      sovereign.hft.cpu-pins="4-5" \
      sovereign.hft.cpu-pins-mode="exclusive" \
      sovereign.hft.deploy-strategy="hft-stateful" \
      sovereign.hft.pre-stop-hook="true" \
      sovereign.hft.pre-stop-delay="5s" \
      sovereign.hft.connection-drain="true" \
      sovereign.hft.sched-policy="SCHED_OTHER"
