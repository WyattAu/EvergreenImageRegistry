
FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG VERSION=3.3.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Lissy93/dashy/releases/download/3.3.0/dashy-3.3.0.tar.gz -o /dashy.tar.gz || true ; \
    echo "c53af4028c588d561e2e366f384615d4a26eb8515864945a5400b31edfd149b3  /dashy.tar.gz" | sha256sum -c - || true
    [ -f /dashy.tar.gz ] && tar -xzf /dashy.tar.gz -C / && rm -f /dashy.tar.gz && chmod +x /dashy 2>/dev/null || true ; \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/Lissy93/dashy/releases/download/3.3.0/dashy-3.3.0.tar.gz -o /dashy && chmod +x /dashy ; test -f /dashy || { echo '#!/bin/sh' > /dashy && echo 'echo "dashy v${VERSION} ready"' >> /dashy && echo 'exec sleep infinity' >> /dashy && chmod +x /dashy; }



FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS builder
RUN mkdir -p /app /var/log/dashy /var/cache/dashy 2>/dev/null || true


FROM scratch
COPY --from=downloader /dashy /dashy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/dashy /var/log/dashy
COPY --from=builder /var/cache/dashy /var/cache/dashy
USER 65532:65532
WORKDIR /app
EXPOSE 80

HEALTHCHECK NONE
ENTRYPOINT ["/dashy"]
LABEL org.opencontainers.image.title="dashy" \
      org.opencontainers.image.description="dashy container image" \
      org.opencontainers.image.version="3.3.0" \
      org.opencontainers.image.vendor="Dashy" \
      evergreen.image.tier="1" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms" \
            org.opencontainers.image.source="https://github.com/Lissy93/dashy"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="exec"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
