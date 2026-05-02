ARG VERSION=latest

FROM osixia/phpldapadmin:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-ldap php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates || true
COPY --from=upstream /var/www/phpldapadmin /opt/phpldapadmin
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/phpldapadmin 2>/dev/null || true

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="ldap-account-manager" org.opencontainers.image.version="1.2.6" org.opencontainers.image.vendor="leenooks" org.opencontainers.image.source="https://github.com/leenooks/phpLDAPadmin" sovereign.image.tier="2" sovereign.image.category="identity" sovereign.image.status="functional" sovereign.constraint.nonroot="true" sovereign.constraint.base="wolfi" sovereign.hft.signal-handling="native" sovereign.hft.shutdown-timeout="5s" sovereign.hft.init-system="none" sovereign.hft.startup-timeout="10000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"

USER 65532:65532

STOPSIGNAL SIGTERM

ENTRYPOINT ["php-fpm"]

CMD ["-F"]
