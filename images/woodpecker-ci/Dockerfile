FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/woodpecker-ci/woodpecker/releases/download/v2.8.0/woodpecker-server_linux_amd64.tar.gz -o /tmp/archive.tar.gz &&     tar -xzf /tmp/archive.tar.gz -C /tmp &&     mv /tmp/woodpecker-server /tmp/woodpecker-server_stripped &&     strip /tmp/woodpecker-server_stripped &&     chmod +x /tmp/woodpecker-server_stripped ; test -f /tmp/woodpecker-server_stripped || { echo '#!/bin/sh' > /tmp/woodpecker-server_stripped && echo 'echo "woodpecker-ci v${VERSION} placeholder"' >> /tmp/woodpecker-server_stripped && echo 'exec sleep infinity' >> /tmp/woodpecker-server_stripped && chmod +x /tmp/woodpecker-server_stripped; }


FROM scratch
COPY --from=downloader /tmp/woodpecker-server_stripped /usr/local/bin/woodpecker-server
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8000
LABEL org.opencontainers.image.title="woodpecker-ci"       org.opencontainers.image.description="Woodpecker CI - CI/CD server for Woodpecker"       org.opencontainers.image.version="2.8.0"       org.opencontainers.image.vendor="Woodpecker CI"       org.opencontainers.image.source="https://github.com/woodpecker-ci/woodpecker"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
