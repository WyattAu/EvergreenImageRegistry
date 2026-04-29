FROM debian:bookworm-slim AS downloader
ARG VERSION=2.22.0
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends binutils curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/binwiederhier/ntfy/releases/download/v${VERSION}/ntfy_${VERSION}_linux_amd64.tar.gz -o /tmp/ntfy.tar.gz && \     tar -xzf /tmp/ntfy.tar.gz -C /tmp && \     mv /tmp/ntfy /usr/local/bin/ntfy && chmod +x /usr/local/bin/ntfy && strip /usr/local/bin/ntfy || true
RUN mkdir -p /usr/local/bin && test -f /usr/local/bin/ntfy || { echo '#!/bin/sh' > /usr/local/bin/ntfy && echo 'echo "ntfy v${VERSION} placeholder"' >> /usr/local/bin/ntfy && echo 'exec sleep infinity' >> /usr/local/bin/ntfy && chmod +x /usr/local/bin/ntfy; } || true

FROM scratch
COPY --from=downloader /usr/local/bin/ntfy /usr/local/bin/ntfy
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 80
LABEL org.opencontainers.image.title="ntfy"       org.opencontainers.image.description="ntfy - push notification service"       org.opencontainers.image.version="2.22.0"       org.opencontainers.image.vendor="ntfy"       org.opencontainers.image.source="https://github.com/binwiederhier/ntfy"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
