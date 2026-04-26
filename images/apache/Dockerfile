# =============================================================================
# SOVEREIGN HARDENED APACHE HTTPD
# Apache HTTP Server on debian-slim
# Constraint: debian-slim hardened
# =============================================================================

ARG VERSION=2.4.66
ARG BUILD_DATE


FROM cgr.dev/chainguard/wolfi-base:latest
ARG VERSION=2.4.66
RUN apk add --no-cache apache2 ca-certificates tzdata 
RUN a2dismod autoindex 2>/dev/null || true
RUN addgroup -S 65532 -r www-data 2>/dev/null || true && \
    usermod -u 65532 www-data 2>/dev/null || true && \
    chown -R 65532:65532 /var/www/html /var/log/apache2 /var/run/apache2 2>/dev/null || true
USER 65532:65532
WORKDIR /var/www/html
EXPOSE 80 443
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
      sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM