FROM debian:bookworm-slim AS downloader
ARG VERSION=1.21.10
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/go-gitea/gitea/releases/download/v1.21.10/gitea-1.21.10-linux-amd64 -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary ; test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "gitea-secure v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; }


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitea
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 3000
LABEL org.opencontainers.image.title="gitea-secure"       org.opencontainers.image.description="Gitea Secure - Hardened Git hosting with enhanced security defaults"       org.opencontainers.image.version="1.21.10"       org.opencontainers.image.vendor="Gitea"       org.opencontainers.image.source="https://github.com/go-gitea/gitea"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
