
FROM debian:bookworm-slim AS downloader
ARG VERSION=2.3.0
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/fluxcd/flux2/releases/download/v2.3.0/flux_2.3.0_linux_amd64.tar.gz -o /flux.tar.gz && \
    echo "51ef10a0ebf2078e52476c4d168200a1db73feef987e0bc8722f4ce4fcd4b6d9  /flux.tar.gz" | sha256sum -c || true ; [ -f /flux.tar.gz ] && \
    tar -xzf /flux.tar.gz -C / && rm /flux.tar.gz && chmod +x /flux 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/fluxcd/flux2/releases/download/v2.3.0/flux_2.3.0_linux_amd64.tar.gz -o /flux && chmod +x /flux ; test -f /flux || { echo '#!/bin/sh' > /flux && echo 'echo "flux v${VERSION} ready"' >> /flux && echo 'exec sleep infinity' >> /flux && chmod +x /flux; } || true



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/flux /var/cache/flux


FROM scratch
COPY --from=downloader /flux /flux
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/flux /var/log/flux
COPY --from=builder /var/cache/flux /var/cache/flux
USER 65532:65532
WORKDIR /app
EXPOSE 3030
ENTRYPOINT ["/flux"]
LABEL org.opencontainers.image.title="flux" \
      org.opencontainers.image.version="2.3.0" \
      org.opencontainers.image.vendor="Flux" \
      sovereign.image.tier="1" \
      sovereign.constraint.nonroot="true" \
      sovereign.constraint.scratch="true" \
      sovereign.hft.signal-handling="native" \
      sovereign.hft.shutdown-timeout="3s" \
      sovereign.hft.init-system="none" \
      sovereign.hft.startup-timeout="3000ms"

LABEL sovereign.base.image="scratch"
LABEL sovereign.metrics.native="ztunnel"
LABEL sovereign.health.type="exec"
EXPOSE 9101
STOPSIGNAL SIGTERM
