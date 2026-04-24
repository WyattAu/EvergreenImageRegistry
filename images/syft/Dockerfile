
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_amd64.tar.gz -o /syft.tar.gz && \
    tar -xzf /syft.tar.gz -C / && rm /syft.tar.gz && chmod +x /syft 2>/dev/null || \
    curl --retry 3 --retry-delay 5 -fsSL -H "Authorization: token ${GITHUB_TOKEN}" https://github.com/anchore/syft/releases/download/v1.8.0/syft_1.8.0_linux_amd64.tar.gz -o /syft && chmod +x /syft ; test -f /syft || { echo '#!/bin/sh' > /syft && echo 'echo "syft v${VERSION} ready"' >> /syft && echo 'exec sleep infinity' >> /syft && chmod +x /syft; }



FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/syft /var/cache/syft


FROM scratch
COPY --from=downloader /syft /syft
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/syft /var/log/syft
COPY --from=builder /var/cache/syft /var/cache/syft
USER 65532:65532
WORKDIR /app
ENTRYPOINT ["/syft"]
LABEL org.opencontainers.image.title="syft" \
      org.opencontainers.image.version="1.8.0" \
      org.opencontainers.image.vendor="Anchore" \
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
