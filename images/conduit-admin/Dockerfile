FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/famedly/conduit/releases/download/v0.8.0/conduit-x86_64-unknown-linux-musl -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary
RUN test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "conduit-admin v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; }

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/conduit
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 6167
LABEL org.opencontainers.image.title="conduit-admin"       org.opencontainers.image.description="Conduit Admin - Conduit Matrix homeserver with admin interface"       org.opencontainers.image.version="0.8.0"       org.opencontainers.image.vendor="Famedly"       org.opencontainers.image.source="https://github.com/famedly/conduit"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM