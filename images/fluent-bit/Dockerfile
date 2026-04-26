# =============================================================================
# SOVEREIGN HARDENED FLUENT-BIT
# Generated from template - Version: 3.2.4
# Constraint: debian-slim with Fluent Bit official apt repo
# =============================================================================

ARG VERSION=3.2.4
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=3.2.4
RUN apk add --no-cache curl ca-certificates \
    curl --retry 3 --retry-delay 5 -fsSL "https://packages.fluentbit.io/${VERSION}/fluent-bit-${VERSION}-linux-x86_64.tar.gz" | \
    tar xz -C /opt && \
    ln -s /opt/fluent-bit-${VERSION} /opt/fluent-bit && \
    ln -s /opt/fluent-bit/bin/fluent-bit /usr/local/bin/fluent-bit
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