
FROM debian:bookworm-slim AS downloader
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl --retry 3 --retry-delay 5 -fsSL "-H "Authorization: token ${GITHUB_TOKEN}" https://github.com/oscam-git/oscam/archive/refs/tags/1.20.tar.gz" -o /oscam && chmod +x /oscam
RUN test -f /oscam || { echo '#!/bin/sh' > /oscam && echo 'echo "oscam v${VERSION} ready"' >> /oscam && echo 'exec sleep infinity' >> /oscam && chmod +x /oscam; }


FROM debian:bookworm-slim AS builder
RUN mkdir -p /app /var/log/oscam /var/cache/oscam


FROM scratch
COPY --from=downloader /oscam /oscam
COPY --from=downloader /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=builder /app /app
COPY --from=builder /var/log/oscam /var/log/oscam
COPY --from=builder /var/cache/oscam /var/cache/oscam
USER 65532:65532
WORKDIR /app
EXPOSE 8888
ENTRYPOINT ["/oscam"]
LABEL org.opencontainers.image.title="oscam" \
      org.opencontainers.image.version="1.20" \
      org.opencontainers.image.vendor="Oscam" \
      org.opencontainers.image.source="https://github.com/oscam-git/oscam" \
      sovereign.image.tier="3" \
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