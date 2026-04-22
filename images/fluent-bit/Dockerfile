# =============================================================================
# SOVEREIGN HARDENED FLUENT-BIT
# Generated from template - Version: 3.2.4
# Constraint: debian-slim with Fluent Bit official apt repo
# =============================================================================

ARG VERSION=3.2.4
ARG BUILD_DATE

FROM cgr.dev/chainguard/wolfi-base:latest  # hadolint ignore=DL3007
RUN apt-get update && apt-get install -y --no-install-recommends gnupg curl ca-certificates && \
    curl -sSL https://packages.fluentbit.io/fluentbit.key | gnupg --dearmor -o /usr/share/keyrings/fluentbit.gnupg && \
    echo "deb [signed-by=/usr/share/keyrings/fluentbit.gnupg] https://packages.fluentbit.io/debian/bookworm bookworm main" > /etc/apt/sources.list.d/fluentbit.list && \
    apt-get update && apt-get install -y --no-install-recommends fluent-bit && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/keyrings/fluentbit.gnupg
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit
USER 65532:65532
WORKDIR /app
EXPOSE 2020
ENTRYPOINT ["fluent-bit"]
LABEL org.opencontainers.image.title="fluent-bit" \
      org.opencontainers.image.version="3.2.4" \
      org.opencontainers.image.vendor="Fluent" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM