# =============================================================================
# SOVEREIGN HARDENED PULSAR
# Generated from template - Version: 3.3.0
# Constraint: official - Apache Pulsar is complex, use official base
# =============================================================================

ARG VERSION=3.3.0
ARG BUILD_DATE

FROM apachepulsar/pulsar:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65532 -g '' pulsar 2>/dev/null || true && \
    chown -R pulsar:pulsar /pulsar/data 2>/dev/null || true
USER pulsar

WORKDIR /pulsar
EXPOSE 6650 8080

LABEL org.opencontainers.image.title="pulsar" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/pulsar" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"

LABEL sovereign.base.image="unrecognized"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="none"
EXPOSE 9101
STOPSIGNAL SIGTERM