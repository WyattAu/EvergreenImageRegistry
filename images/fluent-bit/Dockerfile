# =============================================================================
# SOVEREIGN HARDENED FLUENT-BIT
# Generated from template - Version: 3.2.4
# Constraint: debian-slim with Fluent Bit official apt repo
# =============================================================================

ARG VERSION=3.2.4
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && \
    curl -sSL https://packages.fluentbit.io/fluentbit.key | gpg --dearmor -o /usr/share/keyrings/fluentbit.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/fluentbit.gpg] https://packages.fluentbit.io/debian/bookworm bookworm main" > /etc/apt/sources.list.d/fluentbit.list && \
    apt-get update && apt-get install -y --no-install-recommends fluent-bit && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/keyrings/fluentbit.gpg
RUN mkdir -p /app /var/log/fluent-bit /var/cache/fluent-bit
USER 65534:65534
WORKDIR /app
EXPOSE 2020
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["fluent-bit", "--version"]
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
