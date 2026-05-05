ARG VERSION=latest

FROM osixia/phpldapadmin:${VERSION} AS upstream

FROM cgr.dev/chainguard/wolfi-base@sha256:3258be472764337fd13095bcbb3182da170243b5819fd67ad4c0754590588b31

RUN apk add --no-cache php-8.4-fpm php-ldap php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates || true
COPY --from=upstream /var/www/phpldapadmin /opt/phpldapadmin
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/phpldapadmin 2>/dev/null || true

WORKDIR /app

EXPOSE 8080
EXPOSE 9101

LABEL org.opencontainers.image.title="ldap-account-manager" org.opencontainers.image.version="1.2.6" org.opencontainers.image.vendor="leenooks" org.opencontainers.image.source="https://github.com/leenooks/phpLDAPadmin" evergreen.image.tier="2" evergreen.image.category="identity" evergreen.image.status="functional" evergreen.constraint.nonroot="true" evergreen.constraint.base="wolfi" evergreen.hft.signal-handling="native" evergreen.hft.shutdown-timeout="5s" evergreen.hft.init-system="none" evergreen.hft.startup-timeout="10000ms" \
      org.opencontainers.image.description="ldap-account-manager container image" \
evergreen.base.image="wolfi"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

USER 65532:65532

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -sf http://localhost:8080/ || exit 1
ENTRYPOINT ["php-fpm"]

CMD ["-F"]
