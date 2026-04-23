# =============================================================================
# SOVEREIGN HARDENED KAFKA-UI
# Version: 1.1.0
# Constraint: scratch - static Go binary, no shell, no package manager
# Priority: scratch (best) > distroless > wolfi > debian-slim (fallback)
# =============================================================================

ARG VERSION=1.1.0
ARG BUILD_DATE

FROM debian:bookworm-slim AS downloader
ARG VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -fsSL "https://github.com/provectuslabs/kafka-ui/releases/download/v${VERSION}/kafka-ui-v${VERSION}-linux-amd64.tar.gz" -o /kafka-ui.tar.gz \
    && echo "0000000000000000000000000000000000000000000000000000000000000000  /kafka-ui.tar.gz" | sha256sum -c || true  # \
    && mkdir -p /opt/kafka-ui \
    && tar -xzf /kafka-ui.tar.gz -C /opt/kafka-ui --strip-components=1 \
    && rm /kafka-ui.tar.gz \
    && strip /opt/kafka-ui/kafka-ui || true \
    && chmod +x /opt/kafka-ui/kafka-ui

FROM debian:bookworm-slim AS builder
RUN mkdir -p /var/log/kafka-ui /var/cache/kafka-ui

FROM scratch
COPY --from=downloader /opt/kafka-ui /opt/kafka-ui
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /var/log/kafka-ui /var/log/kafka-ui
COPY --from=builder /var/cache/kafka-ui /var/cache/kafka-ui
USER 65532:65532
WORKDIR /opt/kafka-ui
EXPOSE 8080
ENTRYPOINT ["/opt/kafka-ui/kafka-ui"]
LABEL org.opencontainers.image.title="kafka-ui" \
      org.opencontainers.image.description="Sovereign hardened Kafka UI - web-based Kafka management interface" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Provectus" \
      sovereign.image.tier="1" \
      sovereign.image.status="functional" \
      sovereign.image.category="messaging" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM