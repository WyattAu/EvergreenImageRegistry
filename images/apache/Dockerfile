# =============================================================================
# SOVEREIGN HARDENED APACHE HTTPD
# Apache HTTP Server on debian-slim
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=2.4.66
ARG BUILD_DATE

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        apache2 ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* && \
    a2dismod autoindex 2>/dev/null || true
RUN groupadd -g 65534 -r www-data 2>/dev/null || true && \
    usermod -u 65534 www-data 2>/dev/null || true && \
    chown -R 65534:65534 /var/www/html /var/log/apache2 /var/run/apache2 2>/dev/null || true
USER 65534:65534
WORKDIR /var/www/html
EXPOSE 80 443
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["curl", "-f", "http://localhost/"]
ENTRYPOINT ["apache2ctl"]
CMD ["-D", "FOREGROUND"]
LABEL org.opencontainers.image.title="apache" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.vendor="Apache Software Foundation" \
      org.opencontainers.image.source="https://httpd.apache.org" \
      sovereign.image.tier="2" \
      sovereign.image.status="functional" \
      sovereign.image.category="webserver" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.debian_slim="true"
