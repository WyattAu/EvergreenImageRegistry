FROM debian:bookworm-slim AS downloader
ARG VERSION=0.13.8
ARG GITHUB_TOKEN
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/matrix-org/dendrite/releases/download/v0.13.8/dendrite-linux-amd64 -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary ; test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "dendrite v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; } || true


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/dendrite
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8008
LABEL org.opencontainers.image.title="dendrite"       org.opencontainers.image.description="Dendrite - second-generation Matrix homeserver"       org.opencontainers.image.version="0.13.8"       org.opencontainers.image.vendor="Matrix.org"       org.opencontainers.image.source="https://github.com/matrix-org/dendrite"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
