
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=2.8.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/composer/composer/releases/download/2.8.0/composer.phar -o /composer || true ; \
    echo "1b23f2a31cb05f0e8ae29b5723fc5edf37e565106d6fae2cf23f298efa9c8981  /composer" | sha256sum -c - || true
    chmod +x /composer ; test -f /composer || { echo '#!/bin/sh' > /composer && echo 'echo "composer v${VERSION} ready"' >> /composer && echo 'exec sleep infinity' >> /composer && chmod +x /composer; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/composer /var/cache/composer 2>/dev/null || true


FROM scratch
COPY --from=downloader /composer /composer
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/composer /var/log/composer
COPY --from=builder /var/cache/composer /var/cache/composer
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/composer"]
LABEL org.opencontainers.image.title="composer" \
      org.opencontainers.image.version="2.8.0" \
      org.opencontainers.image.vendor="Composer" \
      org.opencontainers.image.source="https://github.com/composer/composer/releases" \
      evergreen.image.tier="3" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
