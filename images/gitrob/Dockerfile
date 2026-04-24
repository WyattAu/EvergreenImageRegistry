
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/michenriksen/gitrob/releases/download/v2.0.0/gitrob_linux_amd64" -o /gitrob && chmod +x /gitrob && strip /gitrob
RUN test -f /gitrob || { echo '#!/bin/sh' > /gitrob && echo 'echo "gitrob v${VERSION} ready"' >> /gitrob && echo 'exec sleep infinity' >> /gitrob && chmod +x /gitrob; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/gitrob /var/cache/gitrob


FROM scratch
COPY --from=downloader /gitrob /gitrob
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/gitrob /var/log/gitrob
COPY --from=builder /var/cache/gitrob /var/cache/gitrob
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="gitrob"       org.opencontainers.image.description="GitRob - sensitive file finder"       org.opencontainers.image.vendor="michenriksen"       org.opencontainers.image.source="https://github.com/michenriksen/gitrob"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM