# =============================================================================
# SOVEREIGN HARDENED ACTIVEMQ
# Generated from template - Version: 6.1.2
# Constraint: official - Apache ActiveMQ is complex, use official base
# =============================================================================

ARG VERSION=6.1.2
ARG BUILD_DATE

FROM apache/activemq-classic:${VERSION}

# Apply sovereignty hardening
USER root
RUN useradd -m -u 65534 -g '' activemq 2>/dev/null || true && \
    chown -R activemq:activemq /opt/activemq 2>/dev/null || true
USER activemq

WORKDIR /opt/activemq
EXPOSE 61616 8161

LABEL org.opencontainers.image.title="activemq" \
      org.opencontainers.image.version="6.1.2" \
      org.opencontainers.image.vendor="Apache" \
      org.opencontainers.image.source="https://github.com/apache/activemq" \
      sovereign.image.tier="2" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.official="true"