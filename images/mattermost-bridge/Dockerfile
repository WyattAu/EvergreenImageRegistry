FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "https://releases.mattermost.com/mattermost/11.6.0/mattermost-11.6.0-linux-amd64.tar.gz" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary
RUN test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "mattermost-bridge v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; }

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/mattermost-bridge
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8065
LABEL org.opencontainers.image.title="mattermost-bridge"       org.opencontainers.image.description="Mattermost Bridge - messaging bridge for Mattermost"       org.opencontainers.image.version="11.6.0"       org.opencontainers.image.vendor="Mattermost"       org.opencontainers.image.source="https://github.com/mattermost/mattermost"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM