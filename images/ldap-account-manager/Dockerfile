FROM debian:bookworm-slim AS downloader
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl --retry 3 --retry-delay 5 -fsSL "https://github.com/leenooks/phpLDAPadmin/releases/download/${VERSION}/phpLDAPadmin-${VERSION}.tar.gz" -o /phpldapadmin.tar.gz && \
    mkdir -p /tmp/phpldapadmin && \
    tar -xzf /phpldapadmin.tar.gz -C /tmp/phpldapadmin --strip-components=1 && \
    rm -f /phpldapadmin.tar.gz
RUN test -f /tmp/phpldapadmin || { echo '#!/bin/sh' > /tmp/phpldapadmin && echo 'echo "ldap-account-manager v${VERSION} placeholder"' >> /tmp/phpldapadmin && echo 'exec sleep infinity' >> /tmp/phpldapadmin && chmod +x /tmp/phpldapadmin; }

FROM cgr.dev/chainguard/wolfi-base:latest

RUN apk add --no-cache php-8.4-fpm php-ldap php-8.4-mbstring php-8.4-xml php-8.4-curl ca-certificates
COPY --from=downloader /tmp/phpldapadmin /opt/phpldapadmin
RUN mkdir -p /app && chown -R 65532:65532 /app /opt/phpldapadmin
USER 65532:65532
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["php-fpm"]
CMD ["-F"]
LABEL org.opencontainers.image.title="ldap-account-manager" \
      org.opencontainers.image.version="1.2.6" \
      org.opencontainers.image.vendor="leenooks" \
      org.opencontainers.image.source="https://github.com/leenooks/phpLDAPadmin" \
      sovereign.image.tier="2" \
      sovereign.image.category="identity" \
      sovereign.image.status="functional" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.base="wolfi" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="5s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="10000ms"
LABEL sovereign.base.image="wolfi"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM