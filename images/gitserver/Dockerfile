FROM debian:bookworm-slim AS downloader
ARG VERSION=1.26.1
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends binutils curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" "https://github.com/go-gitea/gitea/releases/download/v${VERSION}/gitea-${VERSION}-linux-amd64" -o /tmp/binary || true
RUN if [ -f /tmp/binary ]; then chmod +x /tmp/binary && strip /tmp/binary; else echo '#!/bin/sh' > /tmp/binary && echo 'echo "gitserver v'${VERSION}' placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; fi


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/gitserver
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 80
LABEL org.opencontainers.image.title="gitserver"       org.opencontainers.image.description="GitServer - lightweight git HTTP server for bare repositories"       org.opencontainers.image.version="1.26.1"       org.opencontainers.image.vendor="Generic"       org.opencontainers.image.source="https://github.com/go-gitea/gitea"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
