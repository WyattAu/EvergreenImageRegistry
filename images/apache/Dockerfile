# =============================================================================
# SOVEREIGN HARDENED APACHE
# Generated from template - Version: 2.4.66
# Constraint: debian-slim with apt-installed apache2
# =============================================================================

ARG VERSION=2.4.66
ARG BUILD_DATE

FROM debian:bookworm-slim AS builder
RUN apt-get update && \
    apt-get install -y --no-install-recommends apache2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM debian:bookworm-slim
COPY --from=builder /etc/apache2 /etc/apache2
COPY --from=builder /usr/lib/apache2 /usr/lib/apache2
COPY --from=builder /usr/sbin/apache2 /usr/sbin/apache2
COPY --from=builder /usr/share/apache2 /usr/share/apache2
COPY --from=builder /usr/lib/*/libapr*.so* /usr/lib/
COPY --from=builder /usr/lib/*/libapr-util*.so* /usr/lib/
COPY --from=builder /usr/lib/*/libpcre2*.so* /usr/lib/
RUN apt-get update && apt-get install -y --no-install-recommends \
    libapr1 libaprutil1 libpcre2-8 ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/log/apache2 /var/run/apache2 /var/cache/apache2
USER 65534:65534
WORKDIR /app
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/sbin/apache2", "-v"]
ENTRYPOINT ["/usr/sbin/apache2", "-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.version="2.4.66" \
      org.opencontainers.image.vendor="Apache" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"
