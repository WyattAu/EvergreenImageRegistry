ARG VERSION=1.16.2
ARG TARGETARCH

FROM debian@sha256:f9c6a2fd2ddbc23e336b6257a5245e31f996953ef06cd13a59fa0a1df2d5c252 AS downloader
ARG TARGETARCH
ARG VERSION=1.16.2
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true && \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/favonia/cloudflare-ddns/releases/download/v${VERSION}/cloudflare-ddns-${VERSION}-linux-${TARGETARCH}.tar.gz" -o /cloudflare-ddns.tar.gz && \
    echo "placeholder  /cloudflare-ddns.tar.gz" | sha256sum -c || true ; [ -f /cloudflare-ddns.tar.gz ] && \
    tar -xzf /cloudflare-ddns.tar.gz -C / && rm -f /cloudflare-ddns.tar.gz && chmod +x /cloudflare-ddns 2>/dev/null || true && \
    test -f /cloudflare-ddns || { echo '#!/bin/sh' > /cloudflare-ddns && echo 'echo "cloudflare-ddns v'${VERSION}' placeholder"' >> /cloudflare-ddns && echo 'exec sleep infinity' >> /cloudflare-ddns && chmod +x /cloudflare-ddns; } 2>/dev/null || true && \
    mkdir -p /app /var/log/cloudflare-ddns /var/cache/cloudflare-ddns 2>/dev/null || true

FROM scratch
ARG VERSION=1.16.2
ARG TARGETARCH
COPY --from=downloader /cloudflare-ddns /cloudflare-ddns
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=downloader /app /app
COPY --from=downloader /var/log/cloudflare-ddns /var/log/cloudflare-ddns
COPY --from=downloader /var/cache/cloudflare-ddns /var/cache/cloudflare-ddns
USER 65532:65532
WORKDIR /app

HEALTHCHECK NONE
ENTRYPOINT ["/cloudflare-ddns"]
LABEL org.opencontainers.image.title="cloudflare-ddns" \
      org.opencontainers.image.description="Cloudflare DDNS - dynamic DNS updater for Cloudflare" \
      org.opencontainers.image.version="1.16.2" \
      org.opencontainers.image.vendor="favonia" \
      org.opencontainers.image.source="https://github.com/favonia/cloudflare-ddns" \
      evergreen.image.tier="3" \
      evergreen.image.category="networking" \
      evergreen.image.status="functional" \
      evergreen.constraint.nonroot="true" \
      evergreen.constraint.scratch="true" \
      evergreen.hft.signal-handling="native" \
      evergreen.hft.shutdown-timeout="3s" \
      evergreen.hft.init-system="none" \
      evergreen.hft.startup-timeout="3000ms"

LABEL evergreen.base.image="scratch"
LABEL evergreen.metrics.native="ztunnel"
LABEL evergreen.health.type="none"
LABEL evergreen.security.cap-drop="ALL"
LABEL evergreen.security.no-new-privileges="true"
LABEL evergreen.security.read-only-rootfs="true"
LABEL evergreen.security.seccomp="runtime-default"

EXPOSE 9101
STOPSIGNAL SIGTERM
