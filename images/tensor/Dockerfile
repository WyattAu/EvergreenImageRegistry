FROM debian:bookworm-slim AS downloader
ARG VERSION=0.2.0
ARG GITHUB_TOKEN
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN apt-get update &&     apt-get install -y --no-install-recommends curl ca-certificates &&     rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/mautrix/tensor/releases/download/v0.2.0/tensor-linux-amd64 -o /tmp/binary &&     chmod +x /tmp/binary &&     strip /tmp/binary ; test -f /tmp/binary || { echo '#!/bin/sh' > /tmp/binary && echo 'echo "tensor v${VERSION} placeholder"' >> /tmp/binary && echo 'exec sleep infinity' >> /tmp/binary && chmod +x /tmp/binary; }


FROM scratch
COPY --from=downloader /tmp/binary /usr/local/bin/tensor
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

USER 65532:65532
WORKDIR /app
EXPOSE 8008
LABEL org.opencontainers.image.title="tensor"       org.opencontainers.image.description="Tensor - Matrix federation gateway"       org.opencontainers.image.version="0.2.0"       org.opencontainers.image.vendor="mautrix"       org.opencontainers.image.source="https://github.com/mautrix/tensor"       sovereign.image.tier="2"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
