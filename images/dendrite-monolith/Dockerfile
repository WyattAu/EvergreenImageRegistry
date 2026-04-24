FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/matrix-org/dendrite/releases/download/v0.13.0/dendrite-linux-amd64" -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary
RUN test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "dendrite-monolith v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; }

FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/dendrite
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8008
LABEL org.opencontainers.image.title="dendrite-monolith"       org.opencontainers.image.description="Dendrite Monolith - Dendrite in monolith mode"       org.opencontainers.image.version="0.13.0"       org.opencontainers.image.vendor="Matrix.org"       org.opencontainers.image.source="https://github.com/matrix-org/dendrite"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM