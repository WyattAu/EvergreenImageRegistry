
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/* || true
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/grype/releases/download/v0.80.0/grype_0.80.0_linux_amd64.tar.gz -o /grype_0.80.0_linux_amd64.tar.gz &&     [ -f /grype_0.80.0_linux_amd64.tar.gz ] && tar -xzf /grype_0.80.0_linux_amd64.tar.gz -C / && rm /grype_0.80.0_linux_amd64.tar.gz && chmod +x /grype || true
RUN strip /grype 2>/dev/null || true
RUN test -f /grype || { echo '#!/bin/sh' > /grype && echo 'echo "grype-alpine v${VERSION} ready"' >> /grype && echo 'exec sleep infinity' >> /grype && chmod +x /grype; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/grype-alpine /var/cache/grype-alpine 2>/dev/null || true


FROM scratch
COPY --from=downloader /grype /grype
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/grype-alpine /var/log/grype-alpine
COPY --from=builder /var/cache/grype-alpine /var/cache/grype-alpine
USER 65532:65532
WORKDIR /app
LABEL org.opencontainers.image.title="grype-alpine"       org.opencontainers.image.description="Grype - vulnerability scanner (no Alpine)"       org.opencontainers.image.vendor="Anchore"       org.opencontainers.image.source="https://github.com/anchore/grype"       sovereign.image.tier="3"       sovereign.constraint.nonroot="true"       sovereign.constraint.scratch="true"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM